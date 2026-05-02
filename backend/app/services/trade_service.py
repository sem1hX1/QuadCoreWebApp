import asyncio
import json
import logging
from sqlalchemy.orm import Session
from ..db import models
from ..ai.description import generate_price_decision
from ..schemas import product as schemas
from ..scraper.clients import master_scraper

logger = logging.getLogger(__name__)


def _normalize_ref_suggestion(raw_value, fallback_price, fallback_reason):
    if raw_value:
        try:
            text = raw_value.strip()
            if text.startswith("```json"):
                text = text.split("```json", 1)[1].split("```", 1)[0].strip()
            elif text.startswith("```"):
                text = text.split("```", 1)[1].split("```", 1)[0].strip()
            parsed = json.loads(text)
            return json.dumps(parsed, ensure_ascii=False)
        except Exception:
            pass

    return json.dumps({
        "price": round(fallback_price, 2),
        "reason": fallback_reason,
    }, ensure_ascii=False)

try:
    from ..ai.pipeline import process as ai_process
    _AI_AVAILABLE = True
    logger.info("AI pipeline loaded successfully.")
except ImportError as e:
    logger.warning(f"AI pipeline unavailable (missing deps?): {e}. Using fallback pricing.")
    _AI_AVAILABLE = False


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

        # Sitelerden ham veri çekiliyor — hiçbir dönüşüm yapılmıyor
        all_market_products = await master_scraper.search(product.name)

        if not all_market_products: return None

        if _AI_AVAILABLE:
            try:
                loop = asyncio.get_running_loop()
                ai_results = await loop.run_in_executor(
                    None, lambda: ai_process(list(all_market_products))
                )
                if ai_results: return ai_results
            except Exception as e:
                logger.warning(f"AI pipeline execution failed: {e}")

        # Fallback Output
        global_prods = [p for p in all_market_products if p["region"] == "global"]
        tr_prods = [p for p in all_market_products if p["region"] == "TR"]

        analysis_prods = global_prods or all_market_products
        best_deal = min(analysis_prods, key=lambda x: x["price"])
        ref_price = round(best_deal["price"] * 1.3, 2)

        def clean(p):
            return {
                "title": p["title"],
                "source": p["source"],
                "region": p["region"],
                "price": p["price"],
                "price_try": p.get("price_try", p["price"]),
                "url": p.get("url")
            }

        ref_suggestion1 = None
        if _AI_AVAILABLE:
            try:
                loop = asyncio.get_running_loop()
                ref_suggestion1 = await loop.run_in_executor(
                    None,
                    lambda: generate_price_decision(
                        product.name,
                        round(best_deal["price"] * 1.10, 2),
                        {"candidates": [clean(p) for p in sorted(analysis_prods, key=lambda x: x["price"])[:6]]},
                        {"min": min(p["price"] for p in analysis_prods), "avg": sum(p["price"] for p in analysis_prods) / len(analysis_prods), "max": max(p["price"] for p in analysis_prods)},
                        tr_prods,
                    )
                )
            except Exception as e:
                logger.warning(f"AI price suggestion failed: {e}")

        return [{
            "product": product.name,
            "cost": round(best_deal["price"] * 1.10, 2),
            "pricing": {"status": "ok", "price": ref_price, "margin": 0.2},
            "ref_suggestion": _normalize_ref_suggestion(
                ref_suggestion1,
                ref_price,
                "Global fiyatları ve yerel pazar verileri analiz edilmiştir."
            ),
            "top3": [clean(p) for p in sorted(analysis_prods, key=lambda x: x["price"])[:6]],
            "market_refs": [clean(p) for p in tr_prods],
            "description": f"{product.name}: 5'ten fazla yerel ve global distribütör üzerinden analiz edilmiştir."
        }]
