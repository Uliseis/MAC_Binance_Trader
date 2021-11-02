import nest_asyncio
import pandas as pd
import asyncio
from binance import BinanceSocketManager
from binance.client import Client
import numpy as np
import config

from twython import Twython, TwythonError

client = Twython(config.api_key, config.api_secret)

ST = 7
LT = 25

def getHistoricals(symbol, LT):
    df = pd.DataFrame(client.get_historical_klines(symbol))