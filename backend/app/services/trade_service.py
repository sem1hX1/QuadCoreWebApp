import asyncio
import logging
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import product as schemas
from ..scraper.clients import DigiKeyClient, MouserClient, LCSCClient, TrendyolClient

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
        self.digikey = DigiKeyClient()
        self.mouser = MouserClient()
        self.lcsc = LCSCClient()
        self.trendyol = TrendyolClient()

    async def create_product(self, product_in: schemas.ProductCreate):
        db_product = models.Product(**product_in.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    async def run_full_analysis(self, product_id: int):
        product = self.db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            return None

        results = await asyncio.gather(
            self.digikey.search_product(product.name),
            self.mouser.search_product(product.name),
            self.lcsc.search_product(product.name),
            self.trendyol.search_product(product.name),
        )

        all_market_products = []
        for r in results:
            all_market_products.extend(r)

        if not all_market_products:
            return None

        global_products = [p for p in all_market_products if p["region"] == "global"]
        best_deal = min(global_products or all_market_products, key=lambda x: x["price"])
        suggested_price = round(best_deal["price"] * 0.95, 4)

        if _AI_AVAILABLE:
            try:
                loop = asyncio.get_running_loop()
                ai_results = await loop.run_in_executor(
                    None, lambda: ai_process(list(all_market_products), usd_try=USD_TRY_RATE)
                )
                if ai_results:
                    first = ai_results[0]
                    pricing = first.get("pricing", {})
                    if pricing.get("status") == "ok" and pricing.get("price"):
                        # AI price is in TRY, convert back to USD for response consistency
                        suggested_price = round(pricing["price"] / USD_TRY_RATE, 4)
            except Exception as e:
                logger.warning(f"AI pipeline execution failed, using fallback: {e}")

        analysis = models.Analysis(
            product_id=product.id,
            raw_results=all_market_products,
            suggested_price=suggested_price,
            best_deal_json=best_deal,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return {
            "product_id": product.id,
            "results": all_market_products,
            "suggested_price": suggested_price,
            "best_deal": best_deal,
            "created_at": analysis.created_at,
        }
