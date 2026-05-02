from preprocess import preprocess
from embedding import compute_embeddings
from clustering import cluster_products
from currency import convert_to_try, preload_currencies
from market import analyze_market
from pricing import calculate_cost, calculate_sale_price, suggest_price_by_refs
from ranking import get_top3
from ranking import get_top3_with_market
from description import generate_description, generate_description_cached, generate_price_decision

all_currencies = []

def process(products, market_region="TR"):
    products = preprocess(products)

    source_products = [p for p in products if p["region"] != market_region]
    market_products = [p for p in products if p["region"] == market_region]

    source_products = compute_embeddings(source_products)
    market_products = compute_embeddings(market_products)

    clusters = cluster_products(source_products)

    results = []

    for cluster in clusters:
        global_prices = []
        cluster_core = cluster[0].get("core_model", "")

        matched_market = [
            p for p in market_products
            if p.get("core_model", "") == cluster_core
        ]

        for p in cluster:
            p["price"] = convert_to_try(p["price"], p["currency"])
            global_prices.append(p["price"])

        if not global_prices:
            continue

        market = analyze_market([p["price"] for p in matched_market])
        cost = round(calculate_cost(global_prices), 2)

        ref_suggestion = suggest_price_by_refs(cost, matched_market)

        ai_ref_suggestion = generate_price_decision(cluster[0]["title"], cost, ref_suggestion, market, matched_market)

        pricing = calculate_sale_price(cost, market)

        if pricing.get("status") == "ok":
            pricing["price"] = round(pricing["price"], 2)
            pricing["margin"] = round(pricing["margin"], 3)

        results.append({
            "product": cluster[0]["title"],
            "cost": cost,
            "pricing": pricing,
            "ref_suggestion": ai_ref_suggestion,
            "top3": [clean_product(x) for x in get_top3(cluster)],
            "market_refs": [clean_product(x) for x in matched_market],
            "description": generate_description_cached(cluster[0]),
        })

    return results

def clean_product(p):
    return {
        "title": p["title"],
        "source": p["source"],
        "region": p["region"],
        "price": round(p["price"], 3),
        "price_try": round(p.get("price_try", 2), 2)
    }