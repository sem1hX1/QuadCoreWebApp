import json
import logging
import re
import asyncio
import httpx
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_TIMEOUT = 30

def _parse_price(text: str) -> float:
    if not text: return 0.0
    clean = re.sub(r"[^\d,.]", "", text.strip())
    if not clean: return 0.0
    try:
        if "," in clean and "." in clean:
            if clean.rfind(",") > clean.rfind("."): clean = clean.replace(".", "").replace(",", ".")
            else: clean = clean.replace(",", "")
        elif "," in clean: clean = clean.replace(",", ".")
        return float(clean)
    except: return 0.0

class MasterScraper:
    """FindChips Üzerinden Global Veriyi 'Bi Türlü' Çeken Master Scraper"""
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    async def search(self, part_number: str) -> List[Dict]:
        url = f"https://www.findchips.com/search/{part_number}"
        logger.info(f"Master Scraper searching FindChips: {part_number}")
        results = []
        try:
            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
                resp = await client.get(url, timeout=_TIMEOUT)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    dist_blocks = soup.find_all(class_='distributor-results')
                    
                    for block in dist_blocks:
                        dist_title = block.find(class_='distributor-title')
                        if not dist_title: continue
                        # İsmi sadeleştir
                        raw_name = dist_title.text.strip().split(' ')[0].split('\n')[0]
                        name = re.sub(r'[^a-zA-Z0-9]', '', raw_name)
                        
                        rows = block.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            price_val = 0.0
                            part_name = ""
                            
                            for cell in cells:
                                text = cell.text.strip()
                                # Fiyat tespiti
                                if '$' in text or (re.search(r'\d+[.,]\d+', text) and len(text) < 15):
                                    p = _parse_price(text)
                                    if p > 0: price_val = p
                                # Parça adı tespiti
                                if part_number.upper() in text.upper() and cell.find('a'):
                                    # Başlığı temizle
                                    clean_title = text.replace("Buy Now", "").replace("Part Details", "").replace("\n", " ").strip()
                                    part_name = clean_title
                            
                            if price_val > 0 and part_name:
                                results.append({
                                    "title": part_name, "brand": name, "price": price_val,
                                    "currency": "USD", "region": "global", "source": name, "url": url
                                })
                                break
        except Exception as e:
            logger.error(f"Scrape error: {e}")
        return results

master_scraper = MasterScraper()

class DigiKeyClient:
    async def search_product(self, p): return []
class MouserClient:
    async def search_product(self, p): return []
class LCSCClient:
    async def search_product(self, p): return []
class FarnellClient:
    async def search_product(self, p): return []
