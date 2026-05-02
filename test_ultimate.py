import asyncio
from backend.app.scraper.clients import master_scraper
import logging

logging.basicConfig(level=logging.INFO)

async def test_ultimate():
    part = "74HC595"
    print(f"\n🔍 {part} İçin ULTIMATE SCRAPER Taraması...")
    results = await master_scraper.search(part)
    if results:
        for r in results:
            print(f"[{r['source']}] {r['title']} - ${r['price']}")
    else:
        print("❌ Veri yok.")

if __name__ == "__main__":
    asyncio.run(test_ultimate())
