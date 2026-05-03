from .matching import is_same_product

def cluster_products(products):
    clusters = []

    for p in products:
        placed = False

        for c in clusters:
            if is_same_product(p, c[0]):
                c.append(p)
                placed = True
                break

        if not placed:
            clusters.append([p])

    return clusters