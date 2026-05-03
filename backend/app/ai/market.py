def analyze_market(prices):
    if not prices:
        return None

    return {
        "min": min(prices),
        "avg": sum(prices) / len(prices),
        "max": max(prices),
    }