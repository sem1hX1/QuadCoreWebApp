import asyncio
import sys
import os
import json

# Backend dizinini path'e ekle
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.trade_service import TradeService

async def test_full_logic():
    print("Tam İş Mantığı (Service) Testi Başlatılıyor...")
    db = SessionLocal()
    service = TradeService(db)
    
    try:
        # 1. Mevcut veya yeni ürün al
        product_name = "ESP32"
        print(f"Adım 1: '{product_name}' için analiz başlatılıyor...")
        
        # 2. Analizi çalıştır (Scraper + AI/Fallback)
        # run_full_analysis doğrudan product_id almıyor muydu?
        # api/products.py: analysis = await service.run_full_analysis(product.id)
        
        # Veritabanından id bulalım
        from app.db import models
        product = db.query(models.Product).filter(models.Product.name == product_name).first()
        if not product:
            print("Ürün bulunamadı, oluşturuluyor...")
            from app.schemas.product import ProductCreate
            product = await service.create_product(ProductCreate(name=product_name))
        
        print(f"Ürün ID: {product.id}")
        
        # 3. Analizi çalıştır
        print("Adım 2: Analiz süreci (Scraping dahil) çalıştırılıyor...")
        results = await service.run_full_analysis(product.id)
        
        if results:
            print(f"\nBAŞARILI! {len(results)} analiz sonucu üretildi.")
            print("\nÖrnek Çıktı:")
            print(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
            print("\nHATA: Analiz sonucu boş döndü.")
            
    except Exception as e:
        print(f"\nSİSTEM HATASI: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_full_logic())
