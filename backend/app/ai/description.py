import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from google import genai

logger = logging.getLogger(__name__)

# Load .env from backend/app/ai/.env explicitly
_THIS_DIR = Path(__file__).resolve().parent
_env_file = _THIS_DIR / ".env"
if _env_file.exists():
    load_dotenv(_env_file)

# Support both GEMINI_API_KEY and GOOGLE_API_KEY
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
if api_key:
    api_key = api_key.strip().strip('"').strip("'")

# Free tier'da farklı modeller AYRI quota bucket'larına sahip.
# 2.0 serisini kullanmıyoruz; önce 2.5 flash, sonra 2.5 flash-lite deneriz.
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_MODEL = PRIMARY_MODEL  # Geriye dönük uyumluluk

# Sıralama: en yetenekli → daha hafif/yedek
_FALLBACK_MODELS = [
    PRIMARY_MODEL,
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]
# Tekrarları kaldır, sırayı koru
_seen = set()
MODEL_CHAIN = [m for m in _FALLBACK_MODELS if not (m in _seen or _seen.add(m))]

# Quota'sı dolan modelleri kısa süreliğine devre dışı bırak (cool-down)
_model_cooldown_until = {}  # model_name -> unix_ts
_COOLDOWN_SECONDS = 60 * 30  # 30 dakika

client = genai.Client(api_key=api_key) if api_key else None

_desc_cache = {}
_alternatives_cache = {}
_decision_cache = {}


def _is_rate_limit_error(err: Exception) -> bool:
    msg = str(err)
    return "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower()


def _is_cooled_down(model: str) -> bool:
    expires = _model_cooldown_until.get(model)
    if expires is None:
        return False
    if time.time() >= expires:
        _model_cooldown_until.pop(model, None)
        return False
    return True


def _mark_quota_exhausted(model: str):
    _model_cooldown_until[model] = time.time() + _COOLDOWN_SECONDS
    logger.warning(f"Model {model} quota exhausted, cooling down for {_COOLDOWN_SECONDS}s")


def _generate_with_retry(prompt: str, max_retries: int = 1) -> str:
    """
    Model zincirinde sırayla dener. 429 alırsa o modeli cooldown'a alır,
    bir sonraki modele geçer. Hepsi tükenirse son hatayı fırlatır.
    """
    if client is None:
        raise RuntimeError("Gemini client not configured")

    last_err = None
    available = [m for m in MODEL_CHAIN if not _is_cooled_down(m)]
    if not available:
        # Tüm modeller cooldown'da → yine de zinciri tek tek dene (best-effort)
        available = MODEL_CHAIN

    for model in available:
        for attempt in range(max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                text = (response.text or "").strip()
                if model != PRIMARY_MODEL:
                    logger.info(f"Used fallback model: {model}")
                return text
            except Exception as e:
                last_err = e
                if _is_rate_limit_error(e):
                    if attempt < max_retries:
                        # Aynı model için kısa retry (geçici 429)
                        logger.warning(f"{model} rate-limited, brief retry...")
                        time.sleep(2)
                        continue
                    # Kalıcı quota → bu modeli cooldown'a al, sonrakine geç
                    _mark_quota_exhausted(model)
                    break  # bu model'i bırak, dış for sonraki modele geçecek
                # Başka tip hata — retry kalmışsa dene, yoksa sonraki modele geç
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                logger.warning(f"{model} non-rate-limit error: {e}; trying next model")
                break  # sonraki modele

    raise last_err if last_err else RuntimeError("All Gemini models failed")


def generate_description_cached(product):
    """Aynı ürün modeli için Gemini'yi tekrar çağırmaz — bellekte cache'ler."""
    key = (product.get("core_model") or product.get("title") or "").strip().lower()
    if key and key in _desc_cache:
        return _desc_cache[key]
    desc = generate_description(product)
    if key and desc:
        _desc_cache[key] = desc
    return desc

def _smart_fallback_description(product) -> str:
    """Gemini erişilemediğinde ürün tipine göre daha bilgilendirici bir özet üretir."""
    title = (product.get("title") or "").strip()
    brand = (product.get("brand") or "").strip()
    t = title.lower()

    if any(k in t for k in ["esp32", "esp-32"]):
        hint = "Wi-Fi/Bluetooth destekli düşük güç tüketimli mikrodenetleyici; IoT ve sensör ağları için uygundur."
    elif any(k in t for k in ["esp8266", "nodemcu"]):
        hint = "Wi-Fi destekli düşük maliyetli mikrodenetleyici; basit IoT projeleri için tercih edilir."
    elif "stm32" in t:
        hint = "ARM Cortex-M tabanlı yüksek performanslı 32-bit MCU; gömülü kontrol uygulamalarında yaygın kullanılır."
    elif "arduino" in t:
        hint = "Geliştirme ve prototipleme için popüler MCU kartı; geniş kütüphane ekosistemine sahiptir."
    elif "raspberry" in t or "rpi" in t:
        hint = "Linux çalıştırabilen tek kart bilgisayar; ağ uygulamaları ve görüntü işleme için uygundur."
    elif "atmega" in t or "attiny" in t:
        hint = "Düşük güçlü 8-bit AVR mikrodenetleyici; basit kontrol ve ölçüm devrelerinde kullanılır."
    elif "lcd" in t or "oled" in t or "display" in t or "ekran" in t:
        hint = "Gömülü sistemlerde kullanıcı arayüzü için tercih edilen ekran modülü."
    elif "sensor" in t or "sensör" in t:
        hint = "Çevresel ölçüm ve veri toplama uygulamaları için sensör modülü."
    elif "motor" in t or "servo" in t or "step" in t:
        hint = "Robotik ve hareket kontrol uygulamaları için motor/sürücü bileşeni."
    elif "regülat" in t or "regulator" in t or "lm" in t and any(c.isdigit() for c in t):
        hint = "Güç yönetimi ve gerilim regülasyonu için kullanılan analog bileşen."
    else:
        hint = "Elektronik prototipleme ve gömülü sistem projelerinde kullanılan bileşen."

    prefix = f"{brand} {title}".strip() if brand else title
    return f"{prefix}: {hint}"[:150]


def generate_description(product):
    try:
        if client is None:
            raise RuntimeError("GEMINI_API_KEY not set")

        title = product.get("title", "Bilinmeyen ürün")
        brand = product.get("brand", "")
        source = product.get("source", "")
        region = product.get("region", "")
        price = product.get("price", "?")
        currency = product.get("currency", "TRY")

        prompt = f"""
Sen deneyimli bir elektronik komponent mühendisisin.
Aşağıdaki ürün için Türkçe ve teknik bir mini değerlendirme yaz.

Ürün: {title}
Marka: {brand}
Kaynak: {source}
Bölge: {region}
Fiyat: {price} {currency}

Kurallar:
- KESINLIKLE 1-2 cümle yaz.
- KESINLIKLE 150 karakteri GEÇME.
- Genel/boş cümle kurma, ürün tipine uygun teknik yorum ver.
- Sadece açıklama metni dön, başlık/emoji/json/formatla kullanma.
""".strip()

        text = _generate_with_retry(prompt)
        if not text:
            raise RuntimeError("Empty Gemini response")
        if len(text) > 150:
            text = text[:147] + "..."
        return text

    except Exception as e:
        logger.warning(f"Gemini description failed, using smart fallback: {e}")
        return _smart_fallback_description(product)


def generate_price_decision(product_title, cost, ref_suggestion, market, market_refs):
    try:
        if client is None:
            raise RuntimeError("GEMINI_API_KEY not set")

        cache_key = (product_title or "").strip().lower()
        if cache_key and cache_key in _decision_cache:
            return _decision_cache[cache_key]

        prompt = f"""
Sen bir ürün fiyatlama asistanısın.

Ürün: {product_title}
Maliyet: {cost} TRY

Piyasa özeti:
- Min: {market['min'] if market else 'yok'}
- Avg: {market['avg'] if market else 'yok'}
- Max: {market['max'] if market else 'yok'}

Referanslardan üretilen aday fiyatlar:
{ref_suggestion['candidates'] if ref_suggestion else []}

Kurallar:
- Fiyat maliyetin altında olamaz.
- Mümkünse referans min fiyatın biraz altında veya referans ortalamasına yakın olmalı.
- Tek bir sayı döndür.
- Sadece JSON döndür:
{{
  "price": 0,
  "reason": "kısa açıklama"
}}
"""

        text = _generate_with_retry(prompt)
        if cache_key and text:
            _decision_cache[cache_key] = text
        return text

    except Exception as e:
        logger.warning(f"Gemini price decision failed: {e}")
        return None


def generate_alternatives(product_query: str, top_n: int = 4):
    """
    Aranan ürün için drop-in / parametrik olarak benzer alternatifler önerir.
    Sonuç: [{"name": "...", "reason": "...", "differs": "..."}] formatında liste döner.
    """
    import json

    cache_key = (product_query or "").strip().lower()
    if not cache_key:
        return []
    if cache_key in _alternatives_cache:
        return _alternatives_cache[cache_key]

    if client is None:
        # Gemini yoksa boş döndür — frontend zaten boş listeyi gracefully handle ediyor
        return []

    prompt = f"""
Sen deneyimli bir elektronik komponent uzmanısın.
Kullanıcı şu ürünü arıyor: "{product_query}"

Bu ürüne **parametrik olarak benzer (drop-in / pin-uyumlu / işlevsel eşdeğer)** {top_n} alternatif öner.
Tercihen: aynı paket, aynı temel özellikler, küçük farklılıklar (üretici, kapasite, hız vs.).

KESINLIKLE sadece geçerli JSON dizisi döndür (markdown/açıklama yazma):
[
  {{"name": "ALT-PART-1", "reason": "Aynı pinout ve voltaj, daha ucuz alternatif", "differs": "Üretici farkı: ON Semi"}},
  {{"name": "ALT-PART-2", "reason": "...", "differs": "..."}}
]

Kurallar:
- "name" alanı somut bir parça numarası olmalı (örn. STM32F103C8T6, LM7805CT, ATmega328P-AU).
- "reason" Türkçe, 1 cümle, neden uyumlu olduğunu söyle.
- "differs" Türkçe, 1 kısa cümle, ana farkı belirt (fiyat, üretici, performans vs.).
- En fazla {top_n} öneri.
- Boş alternatif yok.
"""

    try:
        text = _generate_with_retry(prompt)
        if not text:
            return []
        # Markdown fence varsa temizle
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

        data = json.loads(cleaned)
        if not isinstance(data, list):
            return []
        # Sadece beklenen alanları al, sınırla
        cleaned_list = []
        for item in data[:top_n]:
            if not isinstance(item, dict):
                continue
            name = (item.get("name") or "").strip()
            if not name:
                continue
            cleaned_list.append({
                "name": name,
                "reason": (item.get("reason") or "").strip()[:200],
                "differs": (item.get("differs") or "").strip()[:200],
            })

        _alternatives_cache[cache_key] = cleaned_list
        return cleaned_list

    except Exception as e:
        logger.warning(f"Gemini alternatives failed: {e}")
        return []