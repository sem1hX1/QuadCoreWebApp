import httpx
import asyncio
async def main():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://www.findchips.com/search/STM32", timeout=10)
            print(f"Status: {resp.status_code}")
            print(f"Text: {resp.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
asyncio.run(main())
