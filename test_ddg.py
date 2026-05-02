import httpx
import asyncio
from bs4 import BeautifulSoup

async def test_ddg():
    url = "https://duckduckgo.com/html/?q=STM32F103C8T6+site:digikey.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:1000]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ddg())
