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

def get_crypto_volume(crypto_id):
    """
    Fetches the daily trading volume of a cryptocurrency from Coingecko API.
    Returns the daily trading volume as a float.
    """
    url = f'{COINGECKO_API_URL}/coins/{crypto_id}/market_chart?vs_currency=usd&days=1'
    response = requests.get(url)
    data = response.json()

    if 'total_volumes' in data:
        volumes = data['total_volumes']
        if len(volumes) > 0:
            # Get the most recent trading volume
            volume = volumes[-1][1]
            return float(volume)

    return None

def determine_buy_sell(crypto_id):
    """
    Determines whether to buy or sell a cryptocurrency based on a trading strategy.
    In this example, we buy if the daily trading volume exceeds a threshold value.
    Modify this function to implement your own trading strategy.
    """
    price = get_crypto_price(crypto_id)
    volume = get_crypto_volume(crypto_id)

    if price is not None and volume is not None:
        # Example strategy: Buy if volume exceeds $1 million
        if volume > 1_000_000:
            print(f"Buy {crypto_id} at price: ${price:.2f}, volume: ${volume:.2f}")
        else:
            print(f"Do not buy {crypto_id} - volume below threshold")
    else:
        print(f"Failed to fetch data for {crypto_id}")

# Example usage
crypto_ids = ['bitcoin', 'ethereum', 'litecoin']

for crypto_id in crypto_ids:
    determine_buy_sell(crypto_id)
