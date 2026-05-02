"""
Scraper test scripti.

Kullanım (backend klasöründe):
    python test_scrapers.py
    python test_scrapers.py ESP32
    python test_scrapers.py "STM32F103C8T6"
"""

import asyncio
import sys
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

sys.path.insert(0, ".")
from app.scraper.clients import DigiKeyClient, MouserClient, LCSCClient

QUERY = sys.argv[1] if len(sys.argv) > 1 else "ESP32"
W = 62


def header(text: str):
    print(f"\n{'═' * W}")
    print(f"  {text}")
    print(f"{'═' * W}")


def section(source: str, results: list, elapsed: float):
    status = f"{len(results)} ürün  ({elapsed:.1f}s)" if results else f"⚠  Veri alınamadı  ({elapsed:.1f}s)"
    print(f"\n  ── {source} {'─' * (W - len(source) - 6)}")
    print(f"     {status}")
    if results:
        print()
        for i, r in enumerate(results, 1):
            stock = f"  │  Stok: {r['stock']}" if r.get("stock") else ""
            sym = "$" if r["currency"] == "USD" else "₺"
            print(f"     {i}. {r['title']}")
            print(f"        Marka: {r['brand']}  │  {sym}{r['price']:.2f}{stock}")


async def run():
    header(f'Arama: "{QUERY}"')

    clients = [
        ("DigiKey", DigiKeyClient()),
        ("Mouser",  MouserClient()),
        ("LCSC",    LCSCClient()),
    ]

    all_results = []
    for name, client in clients:
        t0 = time.perf_counter()
        results = await client.search_product(QUERY)
        elapsed = time.perf_counter() - t0
        section(name, results, elapsed)
        all_results.extend(results)

    usd = [r for r in all_results if r["currency"] == "USD" and r["price"] > 0]
    if usd:
        best = min(usd, key=lambda x: x["price"])
        print(f"\n{'─' * W}")
        print(f"  En ucuz  →  {best['title']}")
        print(f"             {best['source']}  │  ${best['price']:.2f}")
    print(f"{'═' * W}\n")


if __name__ == "__main__":
    asyncio.run(run())
