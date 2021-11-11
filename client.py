import nest_asyncio
import pandas as pd
import asyncio
from binance import BinanceSocketManager
from binance.client import Client
import numpy as np
from pandas.core.algorithms import quantile
import config

from twython import Twython, TwythonError

'''We're searching for coins which have a Moving Average Crossover.
If Short Term is higher than Long Term, the token is bought. 
Stop Loss and Stop Limit are considered in order to sell tokens.'''

''' Place in a config.py file your api_key and api_secret.
API needs to have permissions to BUYING, SELLING, and WATCHING in crypto market.
Enable Spot & Margin trading
'''
client = Client(config.api_key, config.api_secret)

ST = 7 # Short term
LT = 25 # Long term

def getHistoricals(symbol, LT):
    df = pd.DataFrame(client.get_historical_klines(symbol,'1d',
                                                   str(LT) + 'days ago UTC',
                                                   '1 day ago UTC')) # The avg is calculated every day
    closes = pd.DataFrame(df[4])
    closes.columns = ['Close']
    closes['ST'] = closes.Close.rolling(ST-1).sum() # Getting the sum of the previous (no live price)
    closes['LT'] = closes.Close.rolling(LT-1).sum()
    closes.dropna(inplace=True)
    return closes

# historicals = getHistoricals('BTCUSDT', LT)

def liveSMA(hist, live):
    liveST = (hist['ST'].values + live.Price.values) / ST
    liveLT = (hist['LT'].values + live.Price.values) / LT
    return liveST, liveLT

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

async def main(coin, qty, SL_limit, open_position = False):
    bm = BinanceSocketManager(client)
    ts = bm.trade_socket(coin)
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            if res:
                frame = createframe(res)
                print(frame)
                livest, livelt = liveSMA(historicals, frame)
                if livest > livelt and not open_position:
                    order = client.create_order(symbol=coin,
                        side='BUY',
                        type='MARKET',
                        quantity=qty)
                    print(order)
                    buyprice = float(order['fills'][0]['price'])
                    open_position = True
                if open_position and frame.Price[0] < buyprice * SL_limit or frame.Price[0] > 1.02 * buyprice:
                    order = client.create_order(symbol=coin,
                        side='SELL',
                        type = 'MARKET',
                        quantity=qty)
                    print(order)
                    loop.stop()


if __name__ == '__main__':
    print('Welcome to The Auto SMA Crossover Trader.')
    loop = asyncio.get_event_loop()

    print('Introduce the token you want to trade:\n')
    input_token = input()
    historicals = getHistoricals(input_token, LT)

    print('Token' + input_token + ': Introduce now quantity to be bought:\n')
    input_qty = float(input())

    print('You want to buy: ' + str(input_qty) + ' ' + input_token + '.\n')
    print('Please, enter a Stop Loss price:\n')
    input_stop = float(input())

    loop.run_until_complete(main(input_token,input_qty,input_stop))