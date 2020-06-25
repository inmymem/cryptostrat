import time
import hmac
import hashlib
import requests
import os
from .models import ReferencePrice
from celery.decorators import task
import telegram.bot as telegram


btc_average_public_key = os.environ.get('BITCOIN_AVERAGE_PUBLIC_KEY')
btc_average_secret_key = os.environ.get('BITCOIN_AVERAGE_SECRET_KEY')

get_from_cryptostrat_endpoint = False
if (os.environ['DEBUG'] == 'True'):
    get_from_cryptostrat_endpoint = True
################################################""""""
def get_btcaverage_gbp_last():
    timestamp = int(time.time())
    payload = '{}.{}'.format(timestamp, btc_average_public_key)
    hex_hash = hmac.new(btc_average_secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = '{}.{}'.format(payload, hex_hash)
    url = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTCGBP'
    headers = {'X-Signature': signature}
    try:
        result = (requests.get(url=url, headers=headers)).json()['last']
    except TimeoutError:
        return get_btcaverage_gbp_last()
    return result


def update_gbpbtc_price():
    latest_price = None
    if get_from_cryptostrat_endpoint:
        try:
            latest_price = requests.get(url='https://www.cryptostrat.co.uk/reference_price/gbp').json()
        except:
            print('Unable to update GBP/BTC price. Unble to fetch price from CryptoStrat endpoint.')
        if latest_price:
            try:
                ReferencePrice.objects.update_or_create(
                    currency_pair = 'BTCGBP',
                    defaults = {
                        'price' : float(latest_price),
                    }
                )
            except:
                print('Unable to update GBP/BTC price. Unble to update database table.')
    else:
        try:
            latest_price = get_btcaverage_gbp_last()
        except:
            telegram.send_critical_error_message.delay('Unable to update GBP/BTC price. Unable to fetch price from bitcoinaverage.com. Check the price and bots. Halt trading if necessary.')
        if latest_price:
            try:
                ReferencePrice.objects.update_or_create(
                    currency_pair = 'BTCGBP',
                    defaults = {
                        'price' : float(latest_price),
                    }
                )
            except:
                telegram.send_critical_error_message.delay('Unable to update GBP/BTC price. Unble to update database table. Check the price and bots. Halt trading if necessary.')
#update_gbpbtc_price()
