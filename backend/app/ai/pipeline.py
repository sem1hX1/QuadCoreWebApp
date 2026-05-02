from .preprocess import preprocess
from .embedding import compute_embeddings
from .clustering import cluster_products
from .currency import convert_to_try
from .market import analyze_tr_market
from .pricing import calculate_cost, calculate_sale_price
from .ranking import get_top3, get_top3_with_market
from .description import generate_description_cached

def process(products, usd_try=32):
    products = preprocess(products)
    products = compute_embeddings(products)
    clusters = cluster_products(products)

    print("CLUSTERS:")
    for c in clusters:
        print([p["title"] for p in c])

    results = []

    for cluster in clusters:
        global_prices = []
        tr_prices = []

        for p in cluster:
            p["price_try"] = convert_to_try(p["price"], p["currency"], usd_try)

            if p["region"] == "global":
                global_prices.append(p["price_try"])
            else:
                tr_prices.append(p["price_try"])

        if not global_prices:
            continue

        
        market = analyze_tr_market(tr_prices)
        cost = round(calculate_cost(global_prices), 2)

        pricing = calculate_sale_price(cost, market)
        if pricing.get("status") == "ok":
            pricing["price"] = round(pricing["price"], 2)
            pricing["margin"] = round(pricing["margin"], 3)
            
        results.append({
            "product": cluster[0]["title"],
            "cost": cost,
            "pricing": pricing,
            "top3": [clean_product(x) for x in get_top3_with_market(cluster)],
            "description": generate_description_cached(cluster[0]),
        })

    return results

def clean_product(p):
    return {
        "title": p["title"],
        "source": p["source"],
        "region": p["region"],
        "price": p["price"],
        "price_try": p.get("price_try")
    }