import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import re

def scrape_with_uc(part):
    print(f"Undetected Chromedriver ile {part} taraması başlatılıyor...")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    
    try:
        driver = uc.Chrome(options=options)
        
        # Mouser denemesi
        url = f"https://www.mouser.com/c/?q={part}"
        print(f"Mouser'a gidiliyor: {url}")
        driver.get(url)
        time.sleep(10) # Sayfanın render olması için bolca süre verelim
        
        print(f"Mouser Başlık: {driver.title}")
        
        results = []
        
        # Mouser tablo satırlarını bulmaya çalış
        rows = driver.find_elements(By.CSS_SELECTOR, ".searchResultsTable tr.result-row")
        if not rows:
            rows = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            
        print(f"Mouser'da {len(rows)} satır bulundu.")
        
        for row in rows[:3]:
            try:
                name = row.find_element(By.CSS_SELECTOR, ".mfr-part-num").text.strip()
                price_text = row.find_element(By.CSS_SELECTOR, ".price-col").text.strip()
                print(f"Bulundu: {name} - {price_text}")
                results.append({"source": "Mouser", "title": name, "price": price_text})
            except: continue
            
        # DigiKey denemesi
        dk_url = f"https://www.digikey.com/en/products/result?keywords={part}"
        print(f"DigiKey'e gidiliyor: {dk_url}")
        driver.get(dk_url)
        time.sleep(10)
        
        print(f"DigiKey Başlık: {driver.title}")
        
        dk_rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-testid='data-table-row']")
        print(f"DigiKey'de {len(dk_rows)} satır bulundu.")
        
        for row in dk_rows[:3]:
            try:
                name = row.find_element(By.CSS_SELECTOR, "a[data-testid='data-table-product-number']").text.strip()
                price = row.find_element(By.CSS_SELECTOR, "td[data-testid='data-table-unit-price']").text.strip()
                print(f"Bulundu: {name} - {price}")
                results.append({"source": "DigiKey", "title": name, "price": price})
            except: continue
            
        driver.quit()
        return results
        
    except Exception as e:
        print(f"UC Hatası: {e}")
        return []

if __name__ == "__main__":
    res = scrape_with_uc("STM32")
    print("\nSONUÇLAR:")
    for r in res:
        print(r)
