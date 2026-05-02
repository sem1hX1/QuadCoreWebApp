import httpx
import json

def test_api():
    print("Backend API Arama Testi başlatılıyor...")
    url = "http://127.0.0.1:8000/products/search"
    params = {"q": "ESP32"}
    
    try:
        # Timeout süresini biraz daha uzun tutalım
        response = httpx.get(url, params=params, timeout=20.0)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"BAŞARILI! API'den {len(data)} adet kart verisi döndü.")
            if len(data) > 0:
                sample = data[0]
                print("\nÖrnek Veri (İlk Kart):")
                print(f"- Ürün: {sample['name']}")
                print(f"- Tedarikçi: {sample['supplier']}")
                print(f"- Fiyat: {sample['price']} EUR")
                print(f"- AI Önerisi: {sample['ai']}")
        else:
            print(f"HATA: API {response.status_code} koduyla yanıt verdi.")
            print(f"Yanıt: {response.text}")
            
    except Exception as e:
        print(f"İSTEK HATASI: {str(e)}")

if __name__ == "__main__":
    test_api()
