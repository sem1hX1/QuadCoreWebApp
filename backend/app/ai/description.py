from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

_desc_cache = {}

def generate_description_cached(product):
    key = product.get("core_model") or product["title"]
    if key in _desc_cache:
        return _desc_cache[key]
    desc = generate_description(product)
    _desc_cache[key] = desc
    return desc

def generate_description(product):
    try:
        if client is None:
            raise RuntimeError("GEMINI_API_KEY not set")

        prompt = f"{product['title']} için kısa, teknik ve Türkçe bir açıklama yaz."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return f"{product['brand']} üretimi {product['title']} elektronik projelerde kullanılabilir."