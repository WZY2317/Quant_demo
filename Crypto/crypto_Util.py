import requests
import pandas as pd
import ccxt
from datetime import datetime
import time
pd.set_option('expand_frame_repr', False)


def get_single_ticker_data(symbol):
    ticket_url = 'https://api.binance.com/api/v3/ticker/price'
    try:
        res_obj = requests.get(ticket_url, timeout=15)
    except Exception as e:
        print('error')
        return None
    json_obj = res_obj.json()
    # tickets_df = None
    if res_obj.status_code == 200:
        if 'error_code' in json_obj:
            print('错误码:{}', format(json_obj['error_code']))
        else:
            raw_df = pd.DataFrame(json_obj)
            print(raw_df)
    else:
        print('状态码:{}'.format(res_obj.status_code))


def get_klines_data(symbol, interval):
    klines_url = "https://api.binance.com/api/v3/klines?symbol={}&interval={}".format(
        symbol, interval)
    try:
        res_obj = requests.get(klines_url, timeout=15)
    except Exception as e:
        print('error', e)
        return None
    # ticker_df = None
    if res_obj.status_code == 200:
        json_obj = res_obj.json()
        if 'error_code' in json_obj:
            print('error code{}', format(json_obj['error_code']))
        else:
            raw_df = pd.DataFrame(json_obj)
            raw_df.columns = {'opentime', 'openprice', 'high', 'low', 'endPrice', 'volume',
                              'endtime', 'tradeVolume', 'tradeCount', 'activeBVolume', 'ActiveTurnover', 'ignore'}
            raw_df['symbol'] = format(symbol)
        return raw_df


def get_mutiklines_data(symbols, interval):
    klines_df = pd.DataFrame()
    for symbol in symbols:
        kline_df = get_klines_data(symbol, interval)
        if klines_df is None:
            continue
        klines_df = klines_df.append(kline_df)
    return klines_df


def trangle_profit():
    binance_exchange = ccxt.binance({
        'timeout': 15000,
        'enableRatelimit': True
    })
    markets = binance_exchange.load_markets()
    markets_a = 'BTC'
    markets_b = 'ETH'
    symbols = list(markets.keys())
    symbols_df = pd.DataFrame(data=symbols, columns=['symbols'])
    base_quote_df = symbols_df['symbols'].str.split(pat='/', expand=True)
    base_quote_df.columns = ['base', 'quote']
    # 过滤得到以AB计价的货币
    base_a_list = base_quote_df[base_quote_df['quote']
                                == markets_a]['base'].values.tolist
    base_b_list = base_quote_df[base_quote_df['quote']
                                == markets_b]['base'].values.tolist
    common_base_list = list(set(base_a_list)).intersection(set(base_b_list))
    print('{}and{}have{}个相同的计价货币'.format(
        markets_a, markets_b, len(common_base_list)))
    columns = ['markets A',
               'markets B',
               'markets C',
               'p1',
               'p2',
               'p3',
               'profit(%)']
    results_df = pd.DataFrame(columns=columns)
    last_min = binance_exchange.milliseconds()-60*1000
    for base_coin in common_base_list:
        markets_c = base_coin
        market_a2b_symbol = '{}/{}'.format(markets_b, markets_a)
        market_b2c_symbol = '{}/{}'.format(markets_c, markets_b)
        market_a2c_symbol = '{}/{}'.format(markets_a, markets_c)

    # 获取行情前1分钟的数据
        market_a2b_klines = binance_exchange.fetch_ohlcv(
            market_a2b_symbol, since=last_min, limit=1, timeframe='1m')
        market_b2c_klines = binance_exchange.fetch_ohlcv(
            market_b2c_symbol, since=last_min, limit=1, timeframe='1m')
        market_a2c_klines = binance_exchange.fetch_ohlcv(
            market_a2c_symbol, since=last_min, limit=1, timeframe='1m')
        # 获取行情前一分钟的交易对价格
        p1 = market_a2b_klines[0][4]
        p2 = market_b2c_klines[0][4]
        p3 = market_a2c_klines[0][4]

        profit = (p3/(p1*p2)-1)*1000

        results_df = results_df.append({
            'Market A': markets_a,
            'Market B': markets_b,
            'Market C': markets_c,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'Profit(%)': profit
        }, ignore=True)

        time.sleep(binance_exchange.rateLimit/1000)
        results_df.to_csv('./tri_exchange_results.csv', index=None)
