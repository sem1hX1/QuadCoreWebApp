import re

PACKAGE_RE = re.compile(
    r"\b(dip|soic|qfn|tqfp|sop|tssop|ssop|qfp)\s*-?\s*\d+\b|\bpu\b|\bpdip\b",
    re.IGNORECASE,
)

def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_core_model(text: str) -> str:
    """
    Örnek:
    - ATmega328P-PU Microcontroller -> atmega328
    - ATMEGA328 DIP28 AVR -> atmega328
    """
    t = normalize(text)
    t = PACKAGE_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()

    for token in t.split():
        if any(ch.isdigit() for ch in token):
            # atmega328p -> atmega328
            token = re.sub(r"(?<=\d)[a-z]$", "", token)
            return token

    return ""

def extract_package(text: str) -> str:
    t = normalize(text)
    m = re.search(r"\b(dip|soic|qfn|tqfp|sop|tssop|ssop|qfp)\s*-?\s*(\d+)\b", t)
    if not m:
        return ""
    return f"{m.group(1)}{m.group(2)}"

def preprocess(products):
    for p in products:
        title = p.get("title", "")
        brand = p.get("brand", "")

        p["norm_title"] = normalize(title)
        p["norm_brand"] = normalize(brand)
        p["core_model"] = extract_core_model(title)
        p["package"] = extract_package(title)
        p["numbers"] = re.findall(r"\d+[a-zA-Z]*", title.lower())  # debug/ek bilgi
    return products