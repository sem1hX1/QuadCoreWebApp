import asyncio
import sys
import os

# Backend dizinini path'e ekle
sys.path.append(os.getcwd())

from app.scraper.clients import master_scraper

async def main():
    print("Scraper testi başlatılıyor: 'ESP32'...")
    try:
        results = await master_scraper.search("ESP32")
        print(f"\nBAŞARILI! Toplam {len(results)} sonuç bulundu.")
        for res in results[:3]:
            print(f"- {res['source']} ({res['region']}): {res['title']} | {res['price']} {res.get('currency', 'EUR')}")
    except Exception as e:
        print(f"\nHATA OLUŞTU: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
