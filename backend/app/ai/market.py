def analyze_tr_market(tr_prices):
    if not tr_prices:
        return None

    return {
        "min": min(tr_prices),
        "avg": sum(tr_prices) / len(tr_prices),
        "max": max(tr_prices),
    }