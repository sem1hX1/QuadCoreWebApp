import asyncio
import httpx
from bs4 import BeautifulSoup

async def test_tr_sites(part):
    sites = {
        "Robotistan": f"https://www.robotistan.com/arama?q={part}",
        "Direnc.net": f"https://www.direnc.net/arama?q={part}",
        "Robo90": f"https://www.robo90.com/arama?q={part}",
        "Robolink": f"https://www.robolinkmarket.com/arama?q={part}",
        "Komponentci": f"https://www.komponentci.net/arama?q={part}"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
        for name, url in sites.items():
            print(f"\n--- {name} Deneniyor: {url} ---")
            try:
                resp = await client.get(url)
                print(f"Status: {resp.status_code}")
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    print(f"Title: {soup.title.text.strip() if soup.title else 'Yok'}")
                    # Snippet for selector identification
                    print(f"Body Snippet: {resp.text[:200]}")
                else:
                    print(f"Hata: {resp.status_code}")
            except Exception as e:
                print(f"Hata: {e}")

if __name__ == "__main__":
    asyncio.run(test_tr_sites("STM32"))
