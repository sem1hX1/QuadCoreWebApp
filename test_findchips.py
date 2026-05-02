import httpx
import asyncio

async def test_findchips():
    url = "https://www.findchips.com/search/STM32F103C8T6"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    try:
        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_findchips())
