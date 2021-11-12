# MAC_Binance_Trader


My very first Python Automatic Trader.

Trader is searching for coins which have a graphic Moving Average Crossover. In the statistics of time series, and in particular the stock market technical analysis, a moving-average crossover occurs when, on plotting two moving averages each based on different degrees of smoothing, the traces of these moving averages cross.

If Short Term plot is higher than Long Term plot (crossed), the token is bought. (Possible up trend).
Stop Loss and Stop Limit are considered in order to sell tokens.

IMPORTANT STEPS:
1. Create a Binance API in Binance.
2. Place in a config.py file stored in the same folder than the script your api_key and api_secret.
3. Binance API needs to have permissions to BUYING, SELLING, and WATCHING in crypto market. (Enable Spot & Margin trading)
4. Select the coin you want to watch, quantity to be bought, and Limit orders.
5. When everything is completed bot will stop and transactions should have been successful.
