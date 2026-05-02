import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re

def _parse_price(text):
    clean = re.sub(r"[^\d,.]", "", text.strip())
    if not clean: return 0.0
    try: return float(clean.replace(",", ""))
    except: return 0.0

def scrape_findchips_selenium(part):
    print(f"Selenium ile FindChips üzerinden {part} taraması...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    results = []
    try:
        url = f"https://www.findchips.com/search/{part}"
        driver.get(url)
        time.sleep(8)
        
        sections = driver.find_elements(By.CSS_SELECTOR, ".distributor-results")
        for section in sections:
            try:
                dist_name = section.find_element(By.CSS_SELECTOR, ".distributor-title").text.strip().split(' ')[0]
                rows = section.find_elements(By.CSS_SELECTOR, "tr")
                for row in rows[:2]:
                    part_el = row.find_elements(By.CSS_SELECTOR, ".v-part-name a")
                    price_el = row.find_elements(By.CSS_SELECTOR, ".v-price")
                    if part_el and price_el:
                        results.append({
                            "source": dist_name,
                            "title": part_el[0].text.strip(),
                            "price": _parse_price(price_el[0].text),
                            "region": "global",
                            "url": url
                        })
            except: continue
    except Exception as e:
        print(f"Selenium hatası: {e}")
    finally:
        driver.quit()
    return results

if __name__ == "__main__":
    res = scrape_findchips_selenium("STM32")
    for r in res: print(r)
