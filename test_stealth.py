import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By

def scrape_with_stealth(part):
    print(f"Selenium Stealth ile {part} taraması başlatılıyor...")
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    results = []
    try:
        # Mouser
        url = f"https://www.mouser.com/c/?q={part}"
        print(f"Mouser'a gidiliyor...")
        driver.get(url)
        time.sleep(10)
        print(f"Mouser Başlık: {driver.title}")
        
        items = driver.find_elements(By.CSS_SELECTOR, ".searchResultsTable tr.result-row")
        for item in items[:3]:
            try:
                name = item.find_element(By.CSS_SELECTOR, ".mfr-part-num").text.strip()
                price = item.find_element(By.CSS_SELECTOR, ".price-col").text.strip()
                results.append({"source": "Mouser", "title": name, "price": price})
                print(f"Mouser Bulundu: {name}")
            except: continue

        # DigiKey
        url = f"https://www.digikey.com/en/products/result?keywords={part}"
        print(f"DigiKey'e gidiliyor...")
        driver.get(url)
        time.sleep(10)
        print(f"DigiKey Başlık: {driver.title}")
        # print(f"DigiKey Kaynak: {driver.page_source[:1000]}") # Debug için
        
        # Daha genel bir seçici dene
        items = driver.find_elements(By.CSS_SELECTOR, "tr")
        print(f"DigiKey'de toplam {len(items)} tablo satırı bulundu.")
        
        items = driver.find_elements(By.CSS_SELECTOR, "tr[data-testid='data-table-row']")
        for item in items[:3]:
            try:
                name = item.find_element(By.CSS_SELECTOR, "a[data-testid='data-table-product-number']").text.strip()
                price = item.find_element(By.CSS_SELECTOR, "td[data-testid='data-table-unit-price']").text.strip()
                results.append({"source": "DigiKey", "title": name, "price": price})
                print(f"DigiKey Bulundu: {name}")
            except: continue

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        driver.quit()
    return results

if __name__ == "__main__":
    res = scrape_with_stealth("STM32")
    print("\nSONUÇLAR:")
    for r in res: print(r)
