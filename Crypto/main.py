import pandas as pd
import crypto_Util as cdu


def main():
    symbol = 'BTCUSDT'
    interval = '15m'
    symbols = {'BTCUSDT', 'ETHUSDT'}
    # tickets_df = get_single_ticker_data(symbol)
    # klines_df = get_klines_data(symbol, interval)
    # print("tickets_df")
    # klines_df = cdu.get_mutiklines_data(symbols, interval)
    # klines_df.to_csv('./cryptocoin_sample.csv', index=False)
    # print(klines_df)
    cdu.trangle_profit()


if __name__ == '__main__':
    main()
