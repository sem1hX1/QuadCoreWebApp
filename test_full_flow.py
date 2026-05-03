import asyncio
from backend.app.services.trade_service import TradeService
from backend.app.db.session import SessionLocal
import json

async def test_full_flow():
    from backend.app.db.session import engine
    from backend.app.db.models import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    service = TradeService(db)
    
    from backend.app.schemas.product import ProductCreate
    product = await service.create_product(ProductCreate(name="ATmega328P-PU"))
    
    print(f"--- ATmega328P-PU İçin Tam Analiz Başlatılıyor ---")
    results = await service.run_full_analysis(product.id)
    
    print(json.dumps(results, indent=2, ensure_ascii=False))
    db.close()

if __name__ == "__main__":
    asyncio.run(test_full_flow())
