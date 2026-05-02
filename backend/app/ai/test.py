from pipeline import process

print("Running AI pipeline test...")
products = [
    {
        "title": "ATmega328P-PU Microcontroller",
        "brand": "Microchip",
        "price": 1.2,
        "currency": "USD",
        "region": "global",
        "source": "Mouser"
    },
    {
        "title": "ATmega328P-PU Microcontroller DIP-28",
        "brand": "Microchip",
        "price": 1.4,
        "currency": "USD",
        "region": "global",
        "source": "Digikey"
    },
    {
        "title": "ESP32-Wroom-32e",
        "brand": "Espressive Systems",
        "price": 1.4,
        "currency": "USD",
        "region": "global",
        "source": "Digikey"
    },
    {
        "title": "ATmega328",
        "brand": "Microchip",
        "price": 1.6,
        "currency": "USD",
        "region": "global",
        "source": "Digikey"
    }
]

results = process(products)

print(results)