from bitmart.api_spot import APISpot

if __name__ == '__main__':

    spotAPI = APISpot(timeout=(2, 10))

    # Get a list of all cryptocurrencies on the platform
    spotAPI.get_currencies()

    # Querying aggregated tickers of a particular trading pair
    spotAPI.get_v3_ticker(symbol='BTC_USDT')

    # Get the latest trade records of the specified trading pair
    spotAPI.get_v3_trades(symbol='BTC_USDT', limit=10)
