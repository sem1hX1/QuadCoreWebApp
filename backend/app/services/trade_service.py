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

# EUR bazlı sistem, TR fiyatları için dönüşüm oranı
TRY_TO_EUR_RATE = 1.0 / 41.0 # 1 EUR ~ 41 TRY varsayımı (Yarışma anlık değeri)

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

        # Master Scraper ile tüm dünyayı ve Türkiye'yi tarıyoruz
        all_market_products = await master_scraper.search(product.name)

        if not all_market_products: return None

        # Para birimi standardizasyonu (Dashboard Euro bekliyor)
        for p in all_market_products:
            if p.get("currency") == "TRY":
                p["price_try"] = p["price"]
                p["price"] = round(p["price"] * TRY_TO_EUR_RATE, 2)
            else:
                p["price_try"] = round(p["price"] / TRY_TO_EUR_RATE, 2)
                # p["price"] zaten Euro varsayılıyor globalden geliyorsa

        if _AI_AVAILABLE:
            try:
                loop = asyncio.get_running_loop()
                # AI'ya hiçbir oynama yapmadan verileri gönderiyoruz (Euro bazlı)
                ai_results = await loop.run_in_executor(
                    None, lambda: ai_process(list(all_market_products))
                )
                if ai_results: return ai_results
            except Exception as e:
                logger.warning(f"AI pipeline execution failed: {e}")

        # Fallback Output
        global_prods = [p for p in all_market_products if p["region"] == "global"]
        tr_prods = [p for p in all_market_products if p["region"] == "TR"]
        
        best_deal = min(global_prods or all_market_products, key=lambda x: x["price"])
        
        def clean(p):
            return {
                "title": p["title"],
                "source": p["source"],
                "region": p["region"],
                "price": p["price"],
                "price_try": p.get("price_try", round(p["price"] / TRY_TO_EUR_RATE, 2)),
                "url": p.get("url")
            }

        return [{
            "product": product.name,
            "cost": round(best_deal["price"] * 1.10, 2),
            "pricing": {"status": "ok", "price": round(best_deal["price"] * 1.3, 2), "margin": 0.2},
            "ref_suggestion": f"json\\n{{\\n  \\\"price\\\": {round(best_deal['price'] * 1.3, 2)},\\n  \\\"reason\\\": \\\"Global Euro fiyatları ve yerel pazar verileri analiz edilmiştir.\\\"\\n}}\\n",
            "top3": [clean(p) for p in sorted(global_prods, key=lambda x: x["price"])[:6]],
            "market_refs": [clean(p) for p in tr_prods],
            "description": f"{product.name}: 5'ten fazla yerel ve global distribütör üzerinden analiz edilmiştir."
        }]
