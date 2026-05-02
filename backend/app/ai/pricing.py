def calculate_cost(global_prices_try):
    if not global_prices_try:
        return None

    base = min(global_prices_try)
    shipping = base * 0.10
    tax = base * 0.20
    commission = base * 0.15

    return base + shipping + tax + commission

def calculate_sale_price(cost, market):
    if cost is None:
        return {"status": "no_cost"}

    if not market:
        return {"status": "no_market"}

    min_price = cost * 1.20
    target = market["min"] - 1

    final_price = max(min_price, target)
    final_price = min(final_price, market["avg"])

    if final_price <= cost:
        return {"status": "reject"}

    return {
        "status": "ok",
        "price": final_price,
        "margin": (final_price - cost) / cost,
    }