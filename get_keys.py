import config

from twython import Twython, TwythonError

binance = Twython(config.api_key, config.api_secret)