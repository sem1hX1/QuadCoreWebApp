import asyncio
from playwright.async_api import async_playwright
import re

def _parse_price(text):
    clean = re.sub(r"[^\d,.]", "", text.strip())
    if not clean: return 0.0
    try: return float(clean.replace(",", ""))
    except: return 0.0

async def scrape_playwright(part):
    print(f"Playwright ile {part} taraması...")
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # Mouser
            url = f"https://www.mouser.com/c/?q={part}"
            print(f"Mouser'a gidiliyor...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            print(f"Mouser Başlık: {await page.title()}")
            
            rows = await page.query_selector_all(".searchResultsTable tr.result-row")
            if not rows:
                 rows = await page.query_selector_all(".product-card")
                 
            for row in rows[:3]:
                try:
                    name_el = await row.query_selector(".mfr-part-num, .product-name")
                    price_el = await row.query_selector(".price-col, .unit-price")
                    if name_el and price_el:
                        name = (await name_el.inner_text()).strip()
                        price = (await price_el.inner_text()).strip()
                        results.append({"source": "Mouser", "title": name, "price": _parse_price(price), "url": url})
                        print(f"Mouser Bulundu: {name}")
                except: continue
                
            # DigiKey
            dk_url = f"https://www.digikey.com/en/products/result?keywords={part}"
            print(f"DigiKey'e gidiliyor...")
            await page.goto(dk_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            print(f"DigiKey Başlık: {await page.title()}")
            
            rows = await page.query_selector_all("tr[data-testid='data-table-row']")
            for row in rows[:3]:
                try:
                    name_el = await row.query_selector("a[data-testid='data-table-product-number']")
                    price_el = await row.query_selector("td[data-testid='data-table-unit-price']")
                    if name_el and price_el:
                        name = (await name_el.inner_text()).strip()
                        price = (await price_el.inner_text()).strip()
                        results.append({"source": "DigiKey", "title": name, "price": _parse_price(price), "url": dk_url})
                        print(f"DigiKey Bulundu: {name}")
                except: continue

        except Exception as e:
            print(f"Playwright hatası: {e}")
        finally:
            await browser.close()
    return results

if __name__ == "__main__":
    res = asyncio.run(scrape_playwright("STM32"))
    print("\nSONUÇLAR:")
    for r in res: print(r)
