def get_top3(cluster):
    return sorted(cluster, key=lambda x: x.get("price_try", x["price"]))[:3]

def get_top3_with_market(cluster):
    items = sorted(cluster, key=lambda x: x.get("price_try", x["price"]))
    if len(items) <= 3:
        return items
    return [items[0], items[1], items[-1]]  # en ucuz 2 + en pahalı (genelde TR)