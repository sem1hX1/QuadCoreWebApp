from .preprocess import preprocess
from .embedding import compute_embeddings
from .clustering import cluster_products
from .currency import convert_to_try, preload_currencies
from .market import analyze_tr_market
from .pricing import calculate_cost, calculate_sale_price
from .ranking import get_top3
from .ranking import get_top3_with_market
from .description import generate_description, generate_description_cached

all_currencies = []

def process(products, usd_try=32):
    products = preprocess(products)
    products = compute_embeddings(products)
    clusters = cluster_products(products)

    print("CLUSTERS:")
    for c in clusters:
        print([p["title"] for p in c])

    results = []
    all_currencies = [p["currency"] for p in products]
    preload_currencies(all_currencies)

    for cluster in clusters:
        global_products = []
        tr_products = []

        for p in cluster:
            p["price_try"] = convert_to_try(p["price"], p["currency"])
            if p["region"] == "global":
                global_products.append(p)
            else:
                tr_products.append(p)

        if not global_products:
            continue

        global_prices = [p["price_try"] for p in global_products]
        tr_prices = [p["price_try"] for p in tr_products]

        market = analyze_tr_market(tr_prices)
        cost = round(calculate_cost(global_prices), 2)

        pricing = calculate_sale_price(cost, market)
        if pricing.get("status") == "ok":
            pricing["price"] = round(pricing["price"], 2)
            pricing["margin"] = round(pricing["margin"], 3)
        
        # ref_suggestion oluşturma
        ref_price = pricing.get("price", cost * 1.2)
        ref_suggestion = f"json\\n{{\\n  \\\"price\\\": {ref_price},\\n  \\\"reason\\\": \\\"Maliyet üzerinde ve piyasa minimum fiyatının biraz altında, rekabetçi bir başlangıç fiyatı sunar.\\\"\\n}}\\n"

        results.append({
            "product": cluster[0]["title"],
            "cost": cost,
            "pricing": pricing,
            "ref_suggestion": ref_suggestion,
            "top3": [clean_product(x) for x in sorted(global_products, key=lambda x: x["price_try"])[:3]],
            "market_refs": [clean_product(x) for x in tr_products],
            "description": generate_description_cached(cluster[0]),
        })

    return results

def clean_product(p):
    return {
        "title": p["title"],
        "source": p["source"],
        "region": p["region"],
        "price": p["price"],
        "price_try": round(p.get("price_try", 2), 2)
    }