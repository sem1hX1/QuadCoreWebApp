import httpx
import asyncio

async def test_lcsc_direct():
    # LCSC'nin en güncel ve en az blocklanan endpoint'i
    url = "https://wmsc.lcsc.com/wmsc/search/global?keyword=STM32"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://m.lcsc.com",
        "Referer": "https://m.lcsc.com/"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:1000]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_lcsc_direct())
