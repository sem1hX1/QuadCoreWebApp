import os
from typing import List, Dict
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class DigiKeyClient:
    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"DigiKey searching: {part_number}")
        return [
            {
                "title": f"{part_number} Microcontroller",
                "brand": "Microchip",
                "price": 1.45,
                "currency": "USD",
                "region": "global",
                "source": "DigiKey"
            },
            {
                "title": f"{part_number} Microcontroller SMD",
                "brand": "Microchip",
                "price": 1.65,
                "currency": "USD",
                "region": "global",
                "source": "DigiKey"
            }
        ]

class MouserClient:
    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"Mouser searching: {part_number}")
        return [
            {
                "title": f"{part_number} Microcontroller DIP-28",
                "brand": "Microchip",
                "price": 1.2,
                "currency": "USD",
                "region": "global",
                "source": "Mouser"
            }
        ]

class LCSCClient:
    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"LCSC searching: {part_number}")
        return [
            {
                "title": f"{part_number} IC Chip",
                "brand": "Microchip",
                "price": 0.95,
                "currency": "USD",
                "region": "global",
                "source": "LCSC"
            }
        ]

class TrendyolClient:
    async def search_product(self, part_number: str) -> List[Dict]:
        logger.info(f"Trendyol searching: {part_number}")
        return [
            {
                "title": f"{part_number} Mikrodenetleyici",
                "brand": "Microchip",
                "price": 95.0,
                "currency": "TRY",
                "region": "TR",
                "source": "Trendyol"
            },
            {
                "title": f"{part_number} Entegre Devre",
                "brand": "Microchip",
                "price": 89.9,
                "currency": "TRY",
                "region": "TR",
                "source": "Hepsiburada"
            }
        ]
