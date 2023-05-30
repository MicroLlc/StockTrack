from flask import Flask, render_template
from celery import Celery
import requests

COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
API_KEY = 'YOUR_COINGECKO_API_KEY'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
    # Implementation same as before...

@celery.task
def determine_buy_alerts():
    # Fetch data for each cryptocurrency
    crypto_ids = ['bitcoin', 'ethereum', 'litecoin']
    alerts = []

    for crypto_id in crypto_ids:
        price = get_crypto_price(crypto_id)
        volume = get_crypto_volume(crypto_id)

        if price is not None and volume is not None:
            # Example strategy: Buy if volume exceeds $1 million
            if volume > 1_000_000:
                alerts.append({'crypto_id': crypto_id, 'price': price, 'volume': volume})

    # Send alerts or store results for display on the home page
    # Example: store the alerts in a database or global variable
    # You can also send notifications via email, push notifications, etc.

@app.route('/')
def home():
    # Fetch alerts and pass them to the template for rendering
    # Example: retrieve alerts from the database or global variable
    alerts = []

    return render_template('home.html', alerts=alerts)

@app.route('/fetch-alerts')
def fetch_alerts():
    # Trigger the task to determine buy alerts
    determine_buy_alerts.delay()

    return 'Fetching alerts...'

if __name__ == '__main__':
    app.run(debug=True)
