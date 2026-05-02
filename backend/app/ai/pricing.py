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

def suggest_price_by_refs(cost, market_refs):
    """
    Referans fiyatlara göre mantıklı aday fiyatlar üretir.
    """
    if not market_refs:
        return None

    ref_prices = [p["price_try"] for p in market_refs if p.get("price_try")]

    if not ref_prices:
        return None

    ref_min = min(ref_prices)
    ref_avg = sum(ref_prices) / len(ref_prices)
    ref_max = max(ref_prices)

    min_margin_price = cost * 1.20

    # Piyasayı hafif kıran, ama çok agresif olmayan adaylar
    candidates = [
        round(max(min_margin_price, ref_min - 1), 2),
        round(max(min_margin_price, ref_avg * 0.95), 2),
        round(max(min_margin_price, ref_avg), 2),
        round(max(min_margin_price, min(ref_max, ref_avg * 1.05)), 2),
    ]

    # tekrarları temizle
    candidates = sorted(set(candidates))

    return {
        "ref_min": round(ref_min, 2),
        "ref_avg": round(ref_avg, 2),
        "ref_max": round(ref_max, 2),
        "min_margin_price": round(min_margin_price, 2),
        "candidates": candidates,
    }

