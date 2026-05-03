import httpx
import asyncio
from bs4 import BeautifulSoup

async def inspect_selectors(part):
    sites = {
        "Robotistan": "https://www.robotistan.com/arama?q=",
        "Direnc": "https://www.direnc.net/arama?q=",
        "Robo90": "https://www.robo90.com/arama?q=",
        "Robolink": "https://www.robolinkmarket.com/arama?q=",
        "Komponentci": "https://www.komponentci.net/arama?q="
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        for name, base_url in sites.items():
            print(f"\n--- {name} Analizi ---")
            resp = await client.get(base_url + part)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Ürün isimleri ve fiyatları için olası seçicileri tara
            # Robotistan: .product-item, .price
            # Direnc: .productItem, .productPrice
            # Robo90: .product-item, .price
            # Robolink: .show-case, .price
            # Komponentci: .product-item, .price
            
            # Genel bir tarama yapalım
            items = soup.select('.product-item, .productItem, .show-case, .product-card, .list-product')
            print(f"Genel Seçiciyle Bulunan Ürün Sayısı: {len(items)}")
            
            for item in items[:2]:
                text = item.text.strip().replace('\n', ' ')
                print(f"Ürün Snippet: {text[:100]}")

if __name__ == "__main__":
    asyncio.run(inspect_selectors("STM32"))
