from .preprocess import preprocess
from .embedding import compute_embeddings
from .clustering import cluster_products
from .currency import convert_to_try, preload_currencies
from .market import analyze_market
from .pricing import calculate_cost, calculate_sale_price
from .ranking import get_top3
from .description import generate_description, generate_description_cached

def process(products, usd_try=38):
    products = preprocess(products)
    products = compute_embeddings(products)
    clusters = cluster_products(products)

    results = []

    for cluster in clusters:
        global_products = []
        other_products = []

        for p in cluster:
            p["price_try"] = convert_to_try(p["price"], p["currency"])
            if p["region"] == "global":
                global_products.append(p)
            else:
                other_products.append(p)

        if not global_products:
            continue

        global_prices = [p["price_try"] for p in global_products]

        # Market analizi (Global fiyatlar üzerinden de yapılabilir veya boş bırakılabilir)
        market = analyze_market([p["price_try"] for p in other_products])
        cost = round(calculate_cost(global_prices), 2)

        pricing = calculate_sale_price(cost, market)
        if pricing.get("status") == "ok":
            pricing["price"] = round(pricing["price"], 2)
            pricing["margin"] = round(pricing["margin"], 3)

        ref_price = pricing.get("price", cost * 1.25)
        ref_suggestion = f"json\\n{{\\n  \\\"price\\\": {round(ref_price, 2)},\\n  \\\"reason\\\": \\\"Global piyasa verileri ve lojistik maliyetler optimize edilerek hesaplandı.\\\"\\n}}\\n"

        results.append({
            "product": cluster[0]["title"],
            "cost": cost,
            "pricing": pricing,
            "ref_suggestion": ref_suggestion,
            "top3": [clean_product(x) for x in sorted(global_products, key=lambda x: x["price_try"])[:3]],
            "market_refs": [clean_product(x) for x in other_products],
            "description": generate_description_cached(cluster[0]),
        })

    return results

def clean_product(p):
    return {
        "title": p["title"],
        "source": p["source"],
        "region": p["region"],
        "price": round(p["price"], 2),
        "price_try": round(p.get("price_try", 0), 2),
        "url": p.get("url")
    }