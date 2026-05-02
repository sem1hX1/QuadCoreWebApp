import asyncio
from backend.app.scraper.clients import DigiKeyClient, MouserClient, LCSCClient
import logging

# Logları sessize alalım ki sadece sonuçlar görünsün
logging.getLogger('backend.app.scraper.clients').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)

async def test_scrapers():
    part = "ESP32"
    
    print(f"\n🔍 {part} İçin Canlı Piyasa Taraması Başlatılıyor...")
    print("="*50)

    clients = [DigiKeyClient(), MouserClient(), LCSCClient()]
    
    tasks = [c.search_product(part) for c in clients]
    results = await asyncio.gather(*tasks)

    all_results = []
    for res_list in results:
        all_results.extend(res_list)

    for i, r in enumerate(all_results, 1):
        print(f"[{i}] KAYNAK: {r['source']:<8} | ÜRÜN: {r['title']:<25} | FİYAT: ${r['price']:>5.2f} | BÖLGE: {r['region']}")

    print("="*50)
    best = min(all_results, key=lambda x: x['price'])
    print(f"🏆 EN İYİ TEKLİF: {best['source']} - ${best['price']} ({best['title']})")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_scrapers())
