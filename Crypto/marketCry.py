import numpy as np
import pandas as pd
import datetime
import time
import os
from tqdm import tqdm
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
from datetime import datetime as dt
import statsmodels.formula.api as smf
import statsmodels.api as sm

path = r'C:\Users\26856\Documents\GitHub\Quant_demo\Crypto'

# %% Collecting data
'''
因为coinmarket的api要收费,所以用CoinGecko的api
'''


def timeStamp(timeNum):
    # 格式化数据
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# 获取所有的加密货币的名字
cg = CoinGeckoAPI()
coin_list = cg.get_coins_list()
id_list = []
for dic in coin_list:
    coin_id = dic['id']
    id_list.append(coin_id)

# 开始日期以及终止日期
begin_date = "2020-01-01 000000"
timeArray = time.strptime(begin_date, "%Y-%m-%d %H%M%S")
begin_date = int(time.mktime(timeArray))

end_date = "2023-12-31 000000"
timeArray = time.strptime(end_date, "%Y-%m-%d %H%M%S")
end_date = int(time.mktime(timeArray))

df_total = pd.DataFrame()

# 获取货币市场数据,保存信息到df_total
# 因为不能频繁request所以要等待
count = 0
# for crypto in tqdm(id_list[0:4481]):
# 首先从CoinGecko拿到其拥有的所有加密货币的id，然后写一个便利函数，依次获取不同加密货币的数据即可，
# 每拿到一个加密货币数据后，就存储到统一的DataFrame里，代码具体实现路径如下：
for crypto in tqdm(id_list):
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    price_list = []
    vol_list = []
    mcap_list = []

    info = cg.get_coin_market_chart_range_by_id(
        crypto,
        vs_currency='usd',
        from_timestamp=begin_date,
        to_timestamp=end_date)

    time_list = []
    for row in info['prices']:
        timeNum = row[0]
        timeNum = timeStamp(timeNum)
        time_list.append(timeNum)
        price = row[1]
        price_list.append(price)
    df1['date'] = time_list
    df1['price'] = price_list

    time_list = []
    for row in info['market_caps']:
        timeNum = row[0]
        timeNum = timeStamp(timeNum)
        time_list.append(timeNum)
        mcap = row[1]
        mcap_list.append(mcap)
    df2['date'] = time_list
    df2['mcap'] = mcap_list

    time_list = []
    for row in info['total_volumes']:
        timeNum = row[0]
        timeNum = timeStamp(timeNum)
        time_list.append(timeNum)
        vol = row[1]
        vol_list.append(vol)
    df3['date'] = time_list
    df3['vol'] = vol_list

    df = pd.merge(df1, df2, on='date')
    df = pd.merge(df, df3, on='date')
    df['crypto'] = crypto

    df_total = pd.concat([df_total, df], ignore_index=True)
    count += 1
    if count % 50 == 0:
        time.sleep(60)

df_total.to_csv(path+os.sep+'df_total01.csv', encoding='utf_8_sig')
# 为了节省时间,用三台PC来获取数据
df_01 = pd.read_csv(path+os.sep+'df_total01.csv')
df_02 = pd.read_csv(path+os.sep+'df_total02.csv')
df_03 = pd.read_csv(path+os.sep+'df_total03.csv')

all_data = pd.DataFrame()
all_data = pd.concat([df_01, df_02], ignore_index=True)
all_data = pd.concat([all_data, df_03], ignore_index=True)
# %% 数据清洗和处理
# 过程会花费很多的时间
all_data = all_data.sort_values(by='date')
all_data['date'] = pd.to_datetime(all_data['date'])

# 删除未完备的数据
all_data = all_data.replace(0, np.nan).dropna()

# 一周分为七个日期
print('Dividing weeks...')
week_list = []
for date in tqdm(all_data['date']):
    week = 1
    begin_date = dt.strptime('20200101', '%Y%m%d')
    end_date = begin_date + datetime.timedelta(days=7)
    while (date >= end_date) or (date < begin_date):
        begin_date = end_date
        end_date = begin_date + datetime.timedelta(days=7)
        week += 1
    week_list.append(week)
all_data['week'] = week_list


crypto_list = list(all_data['crypto'].unique())
single_data = pd.DataFrame()
new_all_data = pd.DataFrame()

print('Computing daily return...')
for crypto in tqdm(crypto_list):
    single_data = all_data[all_data['crypto'] == crypto]
    single_data['last_price'] = single_data['price'].shift(1)
    single_data['daily_ret'] = (
        single_data['price']-single_data['last_price'])/single_data['last_price']
    new_all_data = pd.concat([single_data, new_all_data], ignore_index=True)

# 删除不具备完备信息的数据
new_all_data = new_all_data.replace(0, np.nan).dropna()

# 计算因子
df_week = pd.DataFrame()
print('Computing Factors...')
for crypto in tqdm(crypto_list):
    crypto_data = new_all_data[new_all_data['crypto'] == crypto]
    AGE = len(crypto_data)

    for week in list(set(week_list))[1:]:
        data_lag1 = crypto_data[crypto_data['week'] == week-1]
        data = crypto_data[crypto_data['week'] == week]
        if data.empty:
            pass
        else:
            flag = 1
            for dret in data['daily_ret']:
                flag = flag * (dret + 1)
            flag = flag - 1
            df_week = df_week.append([{'crypto': crypto,
                                       'date': data['date'].iloc[-1],
                                       'week': week,
                                       'PRC': np.log(data['price'].iloc[-1]+1),
                                       'MAXDPRC': max(data['price']),
                                       'MCAP': np.log(data['mcap'].iloc[-1]+1),
                                       'mcap': data['mcap'].iloc[-1],
                                       'AGE': AGE,
                                       'VOL': np.log(np.average(data['vol']+1)),
                                       'PRCVOL': np.log(np.average(data['vol']*data['price'])+1),
                                       'STDPRCVOL': np.log(np.std(data['vol']*data['price'])+1),
                                       'week_ret': flag}], ignore_index=False)

df_week_with_lag = pd.DataFrame()
print('Computing laging data....')
for crypto in tqdm(crypto_list):
    crypto_data = df_week[df_week['crypto'] == crypto]
    crypto_data['mcap_lag1'] = crypto_data['mcap'].shift(1)
    crypto_data['week_ret_lag1'] = crypto_data['week_ret'].shift(1)
    crypto_data['week_ret_lag2'] = crypto_data['week_ret'].shift(2)
    crypto_data['week_ret_lag3'] = crypto_data['week_ret'].shift(3)
    crypto_data['week_ret_lag4'] = crypto_data['week_ret'].shift(4)
    crypto_data['week_ret_lag1-4'] = (crypto_data['week_ret_lag1'] + 1)*(crypto_data['week_ret_lag2'] + 1)*(
        crypto_data['week_ret_lag3'] + 1)*(crypto_data['week_ret_lag4'] + 1) - 1
    df_week_with_lag = pd.concat(
        [crypto_data, df_week_with_lag], ignore_index='True')
df_week = df_week_with_lag
df_week = df_week.dropna()

# 获取所有的加密货币市场
week_vs_mcap = df_week.groupby('week')['mcap'].sum()
week_vs_mcap = week_vs_mcap.to_frame()
week_vs_mcap.rename(columns={'mcap': 'all_crypto_mcap'}, inplace=True)
week_vs_mcap['all_crypto_mcap_lag1'] = week_vs_mcap['all_crypto_mcap'].shift(1)
week_vs_mcap['Rm'] = (week_vs_mcap['all_crypto_mcap'] -
                      week_vs_mcap['all_crypto_mcap_lag1']) / week_vs_mcap['all_crypto_mcap_lag1']

df_week = pd.merge(week_vs_mcap, df_week, on='week')


# 转化为周回报率
#
df_week['date'] = list(
    map(lambda x: x.replace(' 08:00:00', ''), df_week['date']))
df_week['date'] = pd.to_datetime(df_week['date'], format="%Y-%m-%d")
df_rf = pd.read_excel(path+os.sep+'US_T-bills.xlsx')
df_week = pd.merge(df_week, df_rf, on='date')
df_week['Rf'] = df_week['Rf']/100/52

df_rf = df_week.groupby('week')['Rf'].mean()
df_rf = df_rf.to_frame()
df_rf.rename(columns={'Rf': 'week_Rf'}, inplace=True)
df_week = pd.merge(df_week, df_rf, on='week')
df_week['CMKT'] = df_week['Rm'] - df_week['week_Rf']

df_week = df_week.dropna()
print(df_week)
df_week.to_csv(r'C:\Users\hp\Desktop\QT Final'+os.sep +
               'df_week.csv', encoding='utf_8_sig')

# %%  Function Define Area


def crypto_select(df, week):
   # 根据上个月的数据
    last_week = week-1
    data = df[df['week'] == last_week]
    data = df[df['mcap'] > 1000000]
    return data


def make_strategy_by_size(data, n):
    if n == 1:
        data['PRC_bins'] = pd.cut(data['PRC'], bins=5, labels=False)
        long = data[data['PRC_bins'] == 0]['crypto']
        short = data[data['PRC_bins'] == 4]['crypto']
    elif n == 2:
        data['MAXDPRC_bins'] = pd.cut(data['MAXDPRC'], bins=5, labels=False)
        long = data[data['MAXDPRC_bins'] == 0]['crypto']
        short = data[data['MAXDPRC_bins'] == 4]['crypto']
    elif n == 3:
        data['AGE_bins'] = pd.cut(data['AGE'], bins=5, labels=False)
        long = data[data['AGE_bins'] == 4]['crypto']
        short = data[data['AGE_bins'] == 0]['crypto']
    elif n == 4:
        data['MCAP_bins'] = pd.cut(data['MCAP'], bins=5, labels=False)
        long = data[data['MCAP_bins'] == 0]['crypto']
        short = data[data['MCAP_bins'] == 4]['crypto']
    return long, short


def cpt_return(x):
    long = x[x['position'] == 'long']
    short = x[x['position'] == 'short']

    long_portfolios = (
        long
        .groupby(['week', 'position'])
        .apply(
            lambda g: pd.Series({
                'portfolio_ew_long': g['week_ret'].mean(),
                'portfolio_vw_long': (g['week_ret'] * g['mcap_lag1']).sum() / g['mcap_lag1'].sum()
            })
        )
    ).reset_index()

    short_portfolios = (
        short
        .groupby(['week', 'position'])
        .apply(
            lambda g: pd.Series({
                'portfolio_ew_short': g['week_ret'].mean(),
                'portfolio_vw_short': (g['week_ret'] * g['mcap_lag1']).sum() / g['mcap_lag1'].sum()
            })
        )
    ).reset_index()

    portfolios = pd.merge(
        long_portfolios, short_portfolios, on='week', how='outer')
    return portfolios


def execute_strategy(long, short, week):
    global portfolio
    long_portfolio = pd.DataFrame()
    short_portfolio = pd.DataFrame()
    dataset = df_week[df_week['week'] == week]

    if long.empty:
        pass
    else:
        long_portfolio = dataset[dataset['crypto'].isin(long)]
        long_portfolio['position'] = 'long'

    if short.empty:
        pass
    else:
        short_portfolio = dataset[dataset['crypto'].isin(short)]
        short_portfolio['position'] = 'short'

    portfolio = pd.concat([long_portfolio, portfolio], ignore_index=True)
    portfolio = pd.concat([short_portfolio, portfolio], ignore_index=True)


def draw_curve_cum_ret(X):
    # make a plot of roc curve
    plt.figure(dpi=150)
    lw = 2
    plt.ylim((round(min(X['cum_vw']), 0), round(max(X['cum_vw']), 0)))
    plt.plot(X['week'], X['cum_vw'], color='navy', lw=lw, label='cum_vw')
    plt.xlabel('Week')
    plt.ylabel('Cumulative Return')
    plt.show()
    return plt.show()


def draw_curve_ret(X):
    plt.figure(dpi=150)
    lw = 2
    plt.ylim((round(min(X['strategy_vw']), 0),
             round(max(X['strategy_vw']), 0)))
    # plt.plot(X['week'], X['strategy_ew'], color='navy',lw=lw,label='strategy_ew')
    plt.plot(X['week'], X['strategy_vw'],
             color='navy', lw=lw, label='strategy_vw')
    plt.xlabel('Week')
    plt.ylabel('Return')
    # plt.savefig(path+os.sep+save_name+'.jpg')
    plt.show()
    # print('Figure was saved to ' + path)
    return plt.show()


def cpt_strategy_ret(df):
    df = df.replace(np.nan, 0)
    df['strategy_vw'] = df['portfolio_vw_long'] - df['portfolio_vw_short']
    df['strategy_ew'] = df['portfolio_ew_long'] - df['portfolio_ew_short']

    plt.rcParams["figure.figsize"] = (10, 7)
    df = df.sort_values('week')
    df['cum_ew'] = (df['strategy_ew'] + 1).cumprod() - 1
    df['cum_vw'] = (df['strategy_vw'] + 1).cumprod() - 1

    draw_curve_cum_ret(df)
    draw_curve_ret(df)

    print('avg_long_ew: ', np.average(df['portfolio_ew_long']))
    print('avg_short_ew: ', np.average(
        list(map(lambda x: -x, df['portfolio_ew_short']))))
    print('avg_long_vw: ', np.average(df['portfolio_vw_long']))
    print('avg_short_vw: ', np.average(
        list(map(lambda x: -x, df['portfolio_vw_short']))))

    return df


def make_strategy_by_momentum(data, lagn):
    # To Decide what cryptocurrency to long or short
    if lagn == 1:
        data['week_ret_lag1_bins'] = pd.cut(
            data['week_ret_lag1'], bins=5, labels=False)
        long = data[data['week_ret_lag1_bins'] == 4]['crypto']
        short = data[data['week_ret_lag1_bins'] == 0]['crypto']
    elif lagn == 2:
        data['week_ret_lag2_bins'] = pd.cut(
            data['week_ret_lag2'], bins=5, labels=False)
        long = data[data['week_ret_lag2_bins'] == 4]['crypto']
        short = data[data['week_ret_lag2_bins'] == 0]['crypto']
    elif lagn == 3:
        data['week_ret_lag3_bins'] = pd.cut(
            data['week_ret_lag3'], bins=5, labels=False)
        long = data[data['week_ret_lag3_bins'] == 4]['crypto']
        short = data[data['week_ret_lag3_bins'] == 0]['crypto']
    elif lagn == 4:
        data['week_ret_lag4_bins'] = pd.cut(
            data['week_ret_lag4'], bins=5, labels=False)
        long = data[data['week_ret_lag4_bins'] == 4]['crypto']
        short = data[data['week_ret_lag4_bins'] == 0]['crypto']
    elif lagn == 5:
        data['week_ret_lag1-4_bins'] = pd.cut(
            data['week_ret_lag1-4'], bins=5, labels=False)
        long = data[data['week_ret_lag1-4_bins'] == 4]['crypto']
        short = data[data['week_ret_lag1-4_bins'] == 0]['crypto']
    return long, short


def make_strategy_by_vol(data, n):
    # To Decide what cryptocurrency to long or short
    if n == 1:
        data['VOL_bins'] = pd.cut(data['VOL'], bins=5, labels=False)
        long = data[data['VOL_bins'] == 0]['crypto']
        short = data[data['VOL_bins'] == 4]['crypto']
    elif n == 2:
        data['PRCVOL_bins'] = pd.cut(data['PRCVOL'], bins=5, labels=False)
        long = data[data['PRCVOL_bins'] == 0]['crypto']
        short = data[data['PRCVOL_bins'] == 4]['crypto']
    return long, short


def make_strategy_by_volatility(data):
    data['STDPRCVOL_bins'] = pd.cut(data['STDPRCVOL'], bins=5, labels=False)
    long = data[data['STDPRCVOL_bins'] == 0]['crypto']
    short = data[data['STDPRCVOL_bins'] == 4]['crypto']
    return long, short


def runregression(result):
    result = pd.merge(
        result, df_week[['week', 'week_Rf', 'CMKT']].drop_duplicates(), on='week')
    result['strategy_vw_rf'] = result['strategy_vw'] - result['week_Rf']
    print(smf.ols('strategy_vw_rf ~ 1 + CMKT', result).fit().summary())


def make_strategy_by_size_bins(data, n, m):
    # Strategy: longs the smallest coins and shorts the largest coins generates
    if n == 1:
        data['PRC_bins'] = pd.cut(data['PRC'], bins=5, labels=False)
        long = data[data['PRC_bins'] == m]['crypto']
    elif n == 2:
        data['MAXDPRC_bins'] = pd.cut(data['MAXDPRC'], bins=5, labels=False)
        long = data[data['MAXDPRC_bins'] == m]['crypto']
    elif n == 3:
        data['AGE_bins'] = pd.cut(data['AGE'], bins=5, labels=False)
        long = data[data['AGE_bins'] == m]['crypto']
    elif n == 4:
        data['MCAP_bins'] = pd.cut(data['MCAP'], bins=5, labels=False)
        long = data[data['MCAP_bins'] == m]['crypto']
    return long


def execute_strategy_bins(long, week):
    global portfolio
    long_portfolio = pd.DataFrame()
    dataset = df_week[df_week['week'] == week]

    if long.empty:
        pass
    else:
        long_portfolio = dataset[dataset['crypto'].isin(long)]
        long_portfolio['position'] = 'long'

    portfolio = pd.concat([long_portfolio, portfolio], ignore_index=True)


def cpt_return_bins(x):
    long = x[x['position'] == 'long']

    long_portfolios = (
        long
        .groupby(['week', 'position'])
        .apply(
            lambda g: pd.Series({
                'portfolio_ew_long': g['week_ret'].mean(),
                'portfolio_vw_long': (g['week_ret'] * g['mcap_lag1']).sum() / g['mcap_lag1'].sum()
            })
        )
    ).reset_index()

    portfolios = long_portfolios
    return portfolios


def cpt_strategy_ret_bins(df):
    df = df.replace(np.nan, 0)
    df['strategy_vw'] = df['portfolio_vw_long']
    df['strategy_ew'] = df['portfolio_ew_long']

    plt.rcParams["figure.figsize"] = (10, 7)
    df = df.sort_values('week')
    df['cum_ew'] = (df['strategy_ew'] + 1).cumprod() - 1
    df['cum_vw'] = (df['strategy_vw'] + 1).cumprod() - 1

    draw_curve_cum_ret(df)
    draw_curve_ret(df)

    print('avg_long_ew: ', np.average(df['portfolio_ew_long']))
    print('avg_long_vw: ', np.average(df['portfolio_vw_long']))

    return df


def make_strategy_by_momentum_bins(data, lagn, m):
    # To Decide what cryptocurrency to long or short
    if lagn == 1:
        data['week_ret_lag1_bins'] = pd.cut(
            data['week_ret_lag1'], bins=5, labels=False)
        long = data[data['week_ret_lag1_bins'] == m]['crypto']
    elif lagn == 2:
        data['week_ret_lag2_bins'] = pd.cut(
            data['week_ret_lag2'], bins=5, labels=False)
        long = data[data['week_ret_lag2_bins'] == m]['crypto']
    elif lagn == 3:
        data['week_ret_lag3_bins'] = pd.cut(
            data['week_ret_lag3'], bins=5, labels=False)
        long = data[data['week_ret_lag3_bins'] == m]['crypto']
    elif lagn == 4:
        data['week_ret_lag4_bins'] = pd.cut(
            data['week_ret_lag4'], bins=5, labels=False)
        long = data[data['week_ret_lag4_bins'] == m]['crypto']
    elif lagn == 5:
        data['week_ret_lag1-4_bins'] = pd.cut(
            data['week_ret_lag1-4'], bins=5, labels=False)
        long = data[data['week_ret_lag1-4_bins'] == m]['crypto']
    return long


def make_strategy_by_vol_bins(data, n, m):
    # To Decide what cryptocurrency to long or short
    if n == 1:
        data['VOL_bins'] = pd.cut(data['VOL'], bins=5, labels=False)
        long = data[data['VOL_bins'] == m]['crypto']
    elif n == 2:
        data['PRCVOL_bins'] = pd.cut(data['PRCVOL'], bins=5, labels=False)
        long = data[data['PRCVOL_bins'] == m]['crypto']
    return long


def make_strategy_by_volatility_bins(data, m):
    data['STDPRCVOL_bins'] = pd.cut(data['STDPRCVOL'], bins=5, labels=False)
    long = data[data['STDPRCVOL_bins'] == m]['crypto']
    return long


# %% Size Characteristics - PRC
'''Firstly, we need generate market capitalization, price, maximum day price, and age.
However, since we collect data from investing.com rather than coinmarketcap.com, some
data are not available such as marketcap. So we DO NOT use the marketcap as one of the
factor. Besides, age is defined as Number of days listed on investing.com.'''

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)


for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_size(data, 1)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
PRC_result = cpt_return(portfolio)
print(PRC_result)
PRC_result = cpt_strategy_ret(PRC_result)
PRC_result.to_csv(path+os.sep+'PRC_result.csv', encoding='utf_8_sig')
runregression(PRC_result)


# %% Size Characteristics - MAXDPRC
portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)


for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_size(data, 2)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
MAXDPRC_result = cpt_return(portfolio)
print(MAXDPRC_result)
MAXDPRC_result = cpt_strategy_ret(MAXDPRC_result)
MAXDPRC_result.to_csv(path+os.sep+'MAXDPRC_result.csv', encoding='utf_8_sig')
runregression(MAXDPRC_result)

# %% Size Characteristics - MCAP
portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)


for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_size(data, 4)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
MCAP_result = cpt_return(portfolio)
print(MCAP_result)
MCAP_result = cpt_strategy_ret(MCAP_result)
MCAP_result.to_csv(path+os.sep+'MCAP_result.csv', encoding='utf_8_sig')
runregression(MCAP_result)

# %% Momentum Characteristics - r1,0
'''Factor:
    past one-, two-, three-, four-, one-to-four-, eight-, 16-, 50-, and 100week returns.'''


portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_momentum(data, 1)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
lag1_result = cpt_return(portfolio)
print(lag1_result)
lag1_result = cpt_strategy_ret(lag1_result)
lag1_result.to_csv(path+os.sep+'lag1_result.csv', encoding='utf_8_sig')
runregression(lag1_result)

# %% Momentum Characteristics - r2,0


portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_momentum(data, 2)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
lag2_result = cpt_return(portfolio)
print(lag2_result)
lag2_result = cpt_strategy_ret(lag2_result)
lag2_result.to_csv(path+os.sep+'lag2_result.csv', encoding='utf_8_sig')
runregression(lag2_result)

# %% Momentum Characteristics - r3,0

df_week_lag3 = df_week[['crypto', 'week', 'week_ret', 'week_ret_lag3']]
df_week_lag3 = df_week_lag3.dropna()

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_momentum(data, 3)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
lag3_result = cpt_return(portfolio)
print(lag3_result)
lag3_result = cpt_strategy_ret(lag3_result)
lag3_result.to_csv(path+os.sep+'lag3_result.csv', encoding='utf_8_sig')
runregression(lag3_result)

# %% Momentum Characteristics - r4,0

df_week_lag4 = df_week[['crypto', 'week', 'week_ret', 'week_ret_lag4']]
df_week_lag4 = df_week_lag4.dropna()

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_momentum(data, 4)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
lag4_result = cpt_return(portfolio)
print(lag4_result)
lag4_result = cpt_strategy_ret(lag4_result)
lag4_result.to_csv(path+os.sep+'lag4_result.csv', encoding='utf_8_sig')
runregression(lag4_result)

# %% Momentum Characteristics - r4,1

df_week_lag1to4 = df_week[['crypto', 'week', 'week_ret', 'week_ret_lag1-4']]
df_week_lag1to4 = df_week_lag1to4.dropna()

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_momentum(data, 5)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
lag1to4_result = cpt_return(portfolio)
print(lag1to4_result)
lag1to4_result = cpt_strategy_ret(lag1to4_result)
lag1to4_result.to_csv(path+os.sep+'lag1to4_result.csv', encoding='utf_8_sig')

runregression(lag1to4_result)

# %% Volume Characteristics-VOL

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_vol(data, 1)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
VOL_result = cpt_return(portfolio)
print(VOL_result)
VOL_result = cpt_strategy_ret(VOL_result)
VOL_result.to_csv(path+os.sep+'VOL_result.csv', encoding='utf_8_sig')
runregression(VOL_result)

# %% Volume Characteristics-PRCVOL

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_vol(data, 2)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
PRCVOL_result = cpt_return(portfolio)
print(PRCVOL_result)
PRCVOL_result = cpt_strategy_ret(PRCVOL_result)
PRCVOL_result.to_csv(path+os.sep+'PRCVOL_result.csv', encoding='utf_8_sig')
runregression(PRCVOL_result)

# %% Volatility Characteristics - STDPRCVOL

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)
short = pd.Series(dtype=float)

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long, short = make_strategy_by_volatility(data)
    # Execute the strategy and save postion in "portfolio"
    execute_strategy(long, short, week)

portfolio = portfolio.dropna()
STDPRCVOL_result = cpt_return(portfolio)
print(STDPRCVOL_result)
STDPRCVOL_result = cpt_strategy_ret(STDPRCVOL_result)
STDPRCVOL_result.to_csv(
    path+os.sep+'STDPRCVOL_result.csv', encoding='utf_8_sig')
runregression(STDPRCVOL_result)


# %% Size Characteristics -bins
portfolio = pd.DataFrame()
long = pd.Series(dtype=float)


bins = 1
size_type = 1
save_name = 'PRC_bins1_result.csv'

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    long = make_strategy_by_size_bins(data, size_type, bins)
    execute_strategy_bins(long, week)

portfolio = portfolio.dropna()
result = cpt_return_bins(portfolio)
print(result)
result = cpt_strategy_ret_bins(result)
result.to_csv(path+os.sep+save_name, encoding='utf_8_sig')
runregression(result)

# %% Momentum Characteristics -bins
portfolio = pd.DataFrame()
long = pd.Series(dtype=float)


bins = 1
lagn_type = 1
save_name = 'lag1_bins1.csv'

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    long = make_strategy_by_momentum_bins(data, lagn_type, bins)
    execute_strategy_bins(long, week)


portfolio = portfolio.dropna()
result = cpt_return_bins(portfolio)
print(result)
result = cpt_strategy_ret_bins(result)
result.to_csv(path+os.sep+save_name, encoding='utf_8_sig')
runregression(result)

# %% Volume Characteristics-bins
portfolio = pd.DataFrame()
long = pd.Series(dtype=float)

# VOL_type: 1>>VOL,2>>PRCVOL
# bins: 0,1,2,3,4

bins = 1
VOL_type = 1
save_name = 'VOL_result_bins1.csv'

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    # To Decide what stock to long or short
    long = make_strategy_by_vol_bins(data, VOL_type, bins)
   # 挖掘市场,保存位置
    execute_strategy_bins(long, week)


portfolio = portfolio.dropna()
result = cpt_return_bins(portfolio)
print(result)
result = cpt_strategy_ret_bins(result)
result.to_csv(path+os.sep+save_name, encoding='utf_8_sig')
runregression(result)

# %% Volatility Characteristics-bins

portfolio = pd.DataFrame()
long = pd.Series(dtype=float)

# Volatility_type: >>STDPRCVOL
# bins: 0,1,2,3,4

bins = 1
save_name = 'STDPRCVOL_result_bins1.csv'

for week in tqdm(range(min(df_week['week'])+1, max(df_week['week'])+1)):
    data = crypto_select(df_week, week)
    long = make_strategy_by_volatility_bins(data, bins)
    execute_strategy_bins(long, week)


portfolio = portfolio.dropna()
result = cpt_return_bins(portfolio)
print(result)
result = cpt_strategy_ret_bins(result)
result.to_csv(path+os.sep+save_name, encoding='utf_8_sig')
runregression(result)
