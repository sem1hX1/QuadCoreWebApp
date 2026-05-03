import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_selenium_mouser():
    print("Selenium Mouser Testi Başlatılıyor...")
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Arka planda çalıştır
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        part = "STM32F103C8T6"
        url = f"https://www.mouser.com/c/?q={part}"
        print(f"URL'ye gidiliyor: {url}")
        driver.get(url)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(5)
        
        print(f"Sayfa başlığı: {driver.title}")
        
        # Ürün isimlerini bulmaya çalış
        elements = driver.find_elements(By.CLASS_NAME, "mfr-part-num")
        if not elements:
            elements = driver.find_elements(By.CLASS_NAME, "product-name")
            
        print(f"Bulunan element sayısı: {len(elements)}")
        for el in elements[:5]:
            print(f"Ürün: {el.text}")
            
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_selenium_mouser()
