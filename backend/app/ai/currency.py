import requests

_cached_rates = {}

def preload_currencies(currencies):
    for c in set(c.lower() for c in currencies):
        if c != "try":
            get_rates(c)

def get_rates(base="usd"):
    base = base.lower()

    # cache kontrol
    if base in _cached_rates:
        return _cached_rates[base]

    urls = [
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.min.json",
        f"https://latest.currency-api.pages.dev/v1/currencies/{base}.json"
    ]

    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            data = res.json()

            if base in data:
                rates = data[base]
                _cached_rates[base] = rates
                return rates

        except Exception:
            continue

    raise Exception("Currency API failed (all fallbacks)")

def convert_to_try(price, currency):
    currency = currency.lower()

    if currency == "try":
        return price

    # base = currency → TRY rate'i direkt al
    rates = get_rates(currency)

    if "try" not in rates:
        raise ValueError(f"TRY not found for base {currency}")

    return price * rates["try"]