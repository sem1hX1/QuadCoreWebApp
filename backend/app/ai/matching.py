from .embedding import similarity

def is_same_product(p1, p2):

    if p1.get("norm_brand") != p2.get("norm_brand"):
        return False

    core1 = p1.get("core_model", "")
    core2 = p2.get("core_model", "")

    if not core1 or not core2:
        return False

    # 1. Aynı core model
    if core1 == core2:
        pkg1 = p1.get("package", "")
        pkg2 = p2.get("package", "")

        if pkg1 and pkg2 and pkg1 != pkg2:
            return False

        return True

    # 2. Yakın model (güvenli)
    if core1.startswith(core2) or core2.startswith(core1):
        if abs(len(core1) - len(core2)) <= 1:
            return True

    # 3. AI fallback (kontrollü)
    if similarity(p1, p2) >= 0.85:
        if core1[:5] == core2[:5]:
            return True

    return False