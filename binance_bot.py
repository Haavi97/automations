from os import getenv

from binance.client import Client
from dotenv import load_dotenv, find_dotenv

from send_email import send_email

# init
load_dotenv(find_dotenv())
api_key = getenv('BINANCE_APIKEY')
api_secret = getenv('BINANCE_SECRETKEY')

client = Client(api_key, api_secret)


def asset_eur(asset):
    user_asset = client.get_asset_balance(asset=asset)
    asset_price = client.get_symbol_ticker(symbol=asset+'EUR')
    user_asset_eur = float(user_asset['free'])*float(asset_price['price'])
    return user_asset_eur


def asset_email(asset):
    subject = 'Your ' + asset + ' holdings: ' + str(asset_eur(asset)) + '€'
    body = subject
    try:
        send_email(subject, body)
    except:
        print('Failed to send email')

def total_holdings():
    account = client.get_account()
    total = 0
    for balance in account['balances']:
        if float(balance['free']) > 0:
            current = balance['asset']
            try:
                total += asset_eur(current)
            except:
                print('Could not convert asset: ' + current)
    return total

def send_total_email():
    subject = 'Your total Binance holdings: ' + str(total_holdings()) + '€'
    body = subject
    try:
        send_email(subject, body)
    except:
        print('Failed to send email')



if __name__ == '__main__':
    send_total_email()
    # asset_email('BTC')
    # asset_email('ETH')
    # asset_email('ADA')
    # user_btc_eur = asset_eur('BTC')
    # user_eth_eur = asset_eur('ETH')
    # user_ada_eur = asset_eur('ADA')
    # print(user_btc_eur)
    # print(user_eth_eur)
    # print(user_ada_eur)
