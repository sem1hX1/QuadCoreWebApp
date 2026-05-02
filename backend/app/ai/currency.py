def convert_to_try(price, currency, usd_try):
    if currency == "TRY":
        return price
    if currency == "USD":
        return price * usd_try
    return price