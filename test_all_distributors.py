import asyncio
from backend.app.scraper.clients import master_scraper
import logging

logging.basicConfig(level=logging.INFO)

async def test_all_distributors():
    part = "ESP32" 
    
    print(f"\n🔍 {part} İçin Global + TR Karma Piyasa Taraması Başlatılıyor...")
    print("="*70)

    results = await master_scraper.search(part)

    if not results:
        print("⚠️ HİÇBİR VERİ ÇEKİLEMEDİ!")
    else:
        for i, r in enumerate(results, 1):
            curr = r.get('currency', 'EUR')
            print(f"[{i}] KAYNAK: {r['source']:<15} | BÖLGE: {r['region']:<6} | ÜRÜN: {r['title'][:30]:<30} | FİYAT: {r['price']:>7.2f} {curr}")

        print("="*70)
        # Sadece Euro olanlar arasında en ucuzu bul (Basitlik için)
        eur_results = [r for r in results if r.get('currency') == 'EUR']
        if eur_results:
            best = min(eur_results, key=lambda x: x['price'])
            print(f"🏆 EN UCUZ GLOBAL TEKLİF: {best['source']} - €{best['price']}")
    
    print("="*70)

if __name__ == "__main__":
    asyncio.run(test_all_distributors())
