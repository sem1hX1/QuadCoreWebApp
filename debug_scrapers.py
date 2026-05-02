import asyncio
from backend.app.scraper.clients import master_scraper
import logging

# Logları sessize alalım
logging.basicConfig(level=logging.INFO)

async def test_scrapers():
    part = "STM32F103C8T6" 
    
    print(f"\n🔍 {part} İçin Master Scraper (FindChips-Based) Taraması Başlatılıyor...")
    print("="*50)

    results = await master_scraper.search(part)

    if not results:
        print("⚠️ HİÇBİR VERİ ÇEKİLEMEDİ!")
    else:
        for i, r in enumerate(results, 1):
            print(f"[{i}] KAYNAK: {r['source']:<15} | ÜRÜN: {r['title']:<25} | FİYAT: ${r['price']:>5.2f}")

        print("="*50)
        best = min(results, key=lambda x: x['price'])
        print(f"🏆 EN İYİ TEKLİF: {best['source']} - ${best['price']} ({best['title']})")
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_scrapers())
