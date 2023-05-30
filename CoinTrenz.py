import requests

COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
API_KEY = 'YOUR_COINGECKO_API_KEY'

def get_crypto_price(crypto_id):
    """
    Fetches the current price of a cryptocurrency from Coingecko API.
    Returns the current price as a float.
    """
    url = f'{COINGECKO_API_URL}/simple/price?ids={crypto_id}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    if crypto_id in data and 'usd' in data[crypto_id]:
        return float(data[crypto_id]['usd'])

    return None

def determine_buy_sell(crypto_id):
    """
    Determines whether to buy or sell a cryptocurrency based on a simple strategy.
    Modify this function to implement your own trading strategy.
    """
    price = get_crypto_price(crypto_id)

    if price is not None:
        # Example strategy: Buy if price is below $1000, sell if price is above $2000
        if price < 1000:
            print(f"Buy {crypto_id} at price: ${price:.2f}")
        elif price > 2000:
            print(f"Sell {crypto_id} at price: ${price:.2f}")
        else:
            print(f"Hold {crypto_id} at price: ${price:.2f}")
    else:
        print(f"Failed to fetch price for {crypto_id}")

# Example usage
crypto_ids = ['bitcoin', 'ethereum', 'litecoin']

for crypto_id in crypto_ids:
    determine_buy_sell(crypto_id)
