import json
import logging
import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_IMPERSONATE = "chrome124"
_TIMEOUT = 20


def _parse_price(text: str) -> float:
    clean = re.sub(r"[^\d,.]", "", text.strip())
    if not clean:
        return 0.0
    dot_pos = clean.rfind(".")
    comma_pos = clean.rfind(",")
    if dot_pos > comma_pos:
        clean = clean.replace(",", "")
    elif comma_pos > dot_pos:
        clean = clean.replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return 0.0


def _find_product_list(obj: Any) -> Any:
    """JSON içinde ürün listesini recursive olarak bul."""
    if isinstance(obj, list) and len(obj) > 0:
        first = obj[0]
        if isinstance(first, dict) and any(
            k in first for k in ("manufacturerPartNumber", "partNumber", "mfgPartNumber", "unitPrice")
        ):
            return obj
    if isinstance(obj, dict):
        for v in obj.values():
            result = _find_product_list(v)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = _find_product_list(item)
            if result is not None:
                return result
    return None


class DigiKeyClient:
    _HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.digikey.com/",
        "DNT": "1",
    }

    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"DigiKey searching: {part_number}")
        url = f"https://www.digikey.com/en/products/result?keywords={part_number}"
        try:
            async with AsyncSession(impersonate=_IMPERSONATE) as session:
                resp = await session.get(url, headers=self._HEADERS, timeout=_TIMEOUT)
                if resp.status_code != 200:
                    logger.warning(f"DigiKey HTTP {resp.status_code}")
                    return []
                soup = BeautifulSoup(resp.text, "html.parser")

                # 1) __NEXT_DATA__ içinde ürün listesi ara
                tag = soup.find("script", {"id": "__NEXT_DATA__"})
                if tag:
                    try:
                        data = json.loads(tag.string)
                        products = _find_product_list(data)
                        if products:
                            results = self._parse_products(products, part_number)
                            if results:
                                logger.info(f"DigiKey: {len(results)} ürün (via __NEXT_DATA__)")
                                return results
                    except Exception:
                        pass

                # 2) Sayfa içindeki tüm JSON bloklarında ürün ara
                for script in soup.find_all("script"):
                    src = script.string or ""
                    if "manufacturerPartNumber" not in src:
                        continue
                    for match in re.finditer(r"\{[^<]{30,}\}", src):
                        try:
                            chunk = json.loads(match.group())
                            products = _find_product_list(chunk)
                            if products:
                                results = self._parse_products(products, part_number)
                                if results:
                                    logger.info(f"DigiKey: {len(results)} ürün (via inline JSON)")
                                    return results
                        except Exception:
                            pass

                logger.warning("DigiKey: ürün listesi bulunamadı")
                return []
        except Exception as e:
            logger.warning(f"DigiKey hata: {e}")
            return []

    def _parse_products(self, products: list, part_number: str) -> List[Dict]:
        results = []
        for p in products[:5]:
            if not isinstance(p, dict):
                continue
            title = (
                p.get("manufacturerPartNumber")
                or p.get("mfgPartNumber")
                or p.get("partNumber")
                or part_number
            )
            mfr = p.get("manufacturer") or {}
            brand = mfr.get("name", "DigiKey") if isinstance(mfr, dict) else str(mfr)
            raw = p.get("unitPrice") or p.get("price") or p.get("unitPriceUsd") or "0"
            price = _parse_price(str(raw))
            results.append({
                "title": title,
                "brand": brand,
                "price": price,
                "currency": "USD",
                "region": "global",
                "source": "Digikey",
            })
        return results


class MouserClient:
    _HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.mouser.com/",
        "DNT": "1",
    }

    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"Mouser searching: {part_number}")
        url = f"https://www.mouser.com/c/?q={part_number}"
        try:
            async with AsyncSession(impersonate=_IMPERSONATE) as session:
                resp = await session.get(url, headers=self._HEADERS, timeout=_TIMEOUT)
                if resp.status_code != 200:
                    logger.warning(f"Mouser HTTP {resp.status_code}")
                    return []

                soup = BeautifulSoup(resp.text, "html.parser")
                results = []

                # Mouser ürün satırları
                rows = soup.select(
                    "tr.search-result-row, "
                    "tr[id*='product'], "
                    "#SearchResultsBody tr, "
                    ".search-results-table tr"
                )
                for row in rows[:8]:
                    part = row.select_one(
                        ".mfr-part-num a, "
                        "[class*='MfrPartNumber'] a, "
                        "[class*='mfr-part'] a, "
                        "td.col-part a"
                    )
                    price = row.select_one(
                        ".price-col span, "
                        "[class*='Price'] span, "
                        ".SearchResultsUSD, "
                        "td.col-price span"
                    )
                    if part and price:
                        p_val = _parse_price(price.get_text(strip=True))
                        if p_val > 0:
                            results.append({
                                "title": part.get_text(strip=True),
                                "brand": "Mouser",
                                "price": p_val,
                                "currency": "USD",
                                "region": "global",
                                "source": "Mouser",
                            })

                if results:
                    logger.info(f"Mouser: {len(results)} ürün bulundu")
                else:
                    logger.warning("Mouser: ürün listesi parse edilemedi (selector uyumsuz olabilir)")
                return results
        except Exception as e:
            logger.warning(f"Mouser hata: {e}")
            return []


class LCSCClient:
    _API_URL = "https://wmsc.lcsc.com/wmsc/search/global"
    _HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.lcsc.com/",
        "Origin": "https://www.lcsc.com",
    }

    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"LCSC searching: {part_number}")
        params = {"keyword": part_number, "currentPage": 1, "pageSize": 10}
        try:
            async with AsyncSession(impersonate=_IMPERSONATE) as session:
                resp = await session.get(
                    self._API_URL, params=params, headers=self._HEADERS, timeout=_TIMEOUT
                )
                resp.raise_for_status()
                data = resp.json()
                products = data.get("result", {}).get("productList", [])
                if not products:
                    logger.warning("LCSC: ürün bulunamadı")
                    return []
                results = []
                for p in products[:5]:
                    pricing = p.get("pricingUsd", [])
                    price = float(pricing[0].get("usdPrice", 0)) if pricing else 0.0
                    results.append({
                        "title": p.get("productModel", part_number),
                        "brand": p.get("productBrandEn", "LCSC"),
                        "price": price,
                        "currency": "USD",
                        "region": "global",
                        "source": "LCSC",
                        "stock": p.get("stockNumber", 0),
                    })
                logger.info(f"LCSC: {len(results)} ürün bulundu")
                return results
        except Exception as e:
            logger.warning(f"LCSC hata: {e}")
            return []
