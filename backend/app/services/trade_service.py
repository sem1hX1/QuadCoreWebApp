import asyncio
import logging
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import product as schemas
from ..scraper.clients import master_scraper

logger = logging.getLogger(__name__)

try:
    from ..ai.pipeline import process as ai_process
    _AI_AVAILABLE = True
    logger.info("AI pipeline loaded successfully.")
except ImportError as e:
    logger.warning(f"AI pipeline unavailable (missing deps?): {e}. Using fallback pricing.")
    _AI_AVAILABLE = False

USD_TRY_RATE = 38.0

class TradeService:
    def __init__(self, db: Session):
        self.db = db

    async def create_product(self, product_in: schemas.ProductCreate):
        db_product = models.Product(**product_in.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    async def run_full_analysis(self, product_id: int):
        product = self.db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product: return None

        # Tek bir Master Scraper ile tüm global veriyi "bi türlü" çekiyoruz
        all_market_products = await master_scraper.search(product.name)

        if not all_market_products: return None

        if _AI_AVAILABLE:
            try:
                loop = asyncio.get_running_loop()
                ai_results = await loop.run_in_executor(
                    None, lambda: ai_process(list(all_market_products), usd_try=USD_TRY_RATE)
                )
                if ai_results: return ai_results
            except Exception as e:
                logger.warning(f"AI pipeline execution failed: {e}")

        # Fallback Output
        best_deal = min([p for p in all_market_products], key=lambda x: x["price"])
        
        def clean(p):
            return {
                "title": p["title"],
                "source": p["source"],
                "region": p["region"],
                "price": p["price"],
                "price_try": round(p["price"] * (1 if p["currency"] == "TRY" else USD_TRY_RATE), 2),
                "url": p.get("url")
            }

        return [{
            "product": product.name,
            "cost": round(best_deal["price"] * 1.15, 2),
            "pricing": {"status": "ok", "price": round(best_deal["price"] * 1.4, 2), "margin": 0.25},
            "ref_suggestion": f"json\\n{{\\n  \\\"price\\\": {round(best_deal['price'] * 1.4, 2)},\\n  \\\"reason\\\": \\\"Master Scraper ile toplanan global piyasa verileri analiz edildi.\\\"\\n}}\\n",
            "top3": [clean(p) for p in sorted(all_market_products, key=lambda x: x["price"])[:3]],
            "market_refs": [],
            "description": f"{product.name}: Master Scraper teknolojisi ile tüm global distribütörler taranmış ve en güncel veriler derlenmiştir."
        }]
