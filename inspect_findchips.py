import httpx
import asyncio
from bs4 import BeautifulSoup
async def main():
    url = "https://www.findchips.com/search/STM32"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url)
        print(f"Status: {resp.status_code}")
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(f"Distributor Titles: {[d.text.strip() for d in soup.select('.distributor-title')]}")
        print(f"Table Rows: {len(soup.select('tr'))}")
asyncio.run(main())
