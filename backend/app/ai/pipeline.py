from .preprocess import preprocess
from .embedding import compute_embeddings
from .clustering import cluster_products
from .market import analyze_market
from .pricing import calculate_cost, calculate_sale_price
from .ranking import get_top3
from .description import generate_description, generate_description_cached

def process(products, usd_try=1.0):
    """
    AI Pipeline: Fiyatları Euro bazında direkt kabul eder, 
    hiçbir kur çevrimi (oynama) yapmaz.
    """
    products = preprocess(products)
    products = compute_embeddings(products)
    clusters = cluster_products(products)

    results = []
    
    for cluster in clusters:
        global_products = cluster
        if not global_products: continue

        # Tüm fiyatlar direkt Euro olarak kabul ediliyor
        prices = [p["price"] for p in global_products]
        
        # Maliyet ve pazar analizi
        cost = round(calculate_cost(prices), 2)
        market = analyze_market(prices)

        pricing = calculate_sale_price(cost, market)
        if pricing.get("status") == "ok":
            pricing["price"] = round(pricing["price"], 2)
            pricing["margin"] = round(pricing["margin"], 3)
        
        # Euro bazlı öneri
        ref_price = pricing.get("price", cost * 1.25)
        ref_suggestion = f"json\\n{{\\n  \\\"price\\\": {round(ref_price, 2)},\\n  \\\"reason\\\": \\\"Avrupa distribütörlerinden çekilen saf Euro fiyatları baz alınmıştır.\\\"\\n}}\\n"

        results.append({
            "product": cluster[0]["title"],
            "cost": cost,
            "pricing": pricing,
            "ref_suggestion": ref_suggestion,
            "top3": [clean_product(x) for x in sorted(global_products, key=lambda x: x["price"])[:6]],
            "market_refs": [],
            "description": generate_description_cached(cluster[0]),
        })

    return results

def clean_product(p):
    return {
        "title": p["title"],
        "source": p["source"],
        "region": p["region"],
        "price": round(p["price"], 2),
        "price_try": round(p["price"], 2), # Şemayı bozmamak için Euro değerini buraya da yazıyoruz
        "url": p.get("url")
    }
