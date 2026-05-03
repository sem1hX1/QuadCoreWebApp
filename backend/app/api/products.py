from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ..db.session import get_db
from ..db import models as db_models
from ..schemas import product as schemas
from ..services.trade_service import TradeService

router = APIRouter(prefix="/products", tags=["Products & Analysis"])


@router.get("/alternatives", response_model=List[Dict])
async def get_alternatives(q: str):
    """Aranan ürün için drop-in / parametrik olarak benzer alternatifler önerir."""
    try:
        from ..ai.description import generate_alternatives
        return generate_alternatives(q)
    except Exception:
        return []


@router.get("/currency-rates", response_model=Dict)
async def get_currency_rates():
    """TRY base alınarak EUR ve USD kurlarını döner (frontend currency selector için)."""
    try:
        from ..ai.currency import get_rates
        rates = get_rates("try")
        return {
            "base": "TRY",
            "TRY": 1.0,
            "EUR": float(rates.get("eur", 0)) or None,
            "USD": float(rates.get("usd", 0)) or None,
        }
    except Exception:
        # Canlı kur alınamazsa makul varsayılanlar (yaklaşık 2026 değerleri)
        return {
            "base": "TRY",
            "TRY": 1.0,
            "EUR": 1 / 45.0,  # 1 TRY ≈ 0.022 EUR
            "USD": 1 / 40.0,  # 1 TRY ≈ 0.025 USD
        }


@router.get("/search", response_model=List[schemas.AIAnalysisResult])
async def search_and_analyze(q: str, db: Session = Depends(get_db)):
    """Ürün adına göre arama yapar ve AI analizi çalıştırır."""
    product = db.query(db_models.Product).filter(db_models.Product.name == q).first()
    if not product:
        service = TradeService(db)
        product = await service.create_product(schemas.ProductCreate(name=q))

    service = TradeService(db)
    analysis = await service.run_full_analysis(product.id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"'{q}' için veri bulunamadı.")
    return analysis


@router.post("/", response_model=schemas.ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_new_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    service = TradeService(db)
    return await service.create_product(product)


@router.post("/{product_id}/analyze", response_model=List[schemas.AIAnalysisResult])
async def perform_analysis(product_id: int, db: Session = Depends(get_db)):
    service = TradeService(db)
    analysis_data = await service.run_full_analysis(product_id)
    if not analysis_data:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı veya veri yok.")
    return analysis_data


@router.get("/", response_model=List[schemas.ProductSchema])
async def list_products(db: Session = Depends(get_db)):
    return db.query(db_models.Product).all()
