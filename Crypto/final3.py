import asyncio
import logging
import json
import websocket
from threading import Thread
from binance.lib.utils import config_logging
from binance.error import ClientError
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from websocket_client import BinanceWebsocketClient
from binance.um_futures import UMFutures
config_logging(logging, logging.DEBUG)
#这是我用于记录的博客,建议面试官可以先看看.
#https://juejin.cn/post/7327227246618558503
#我在之前写量化交易的时候,常常使用的是http的连接,通过request来获取数据,但是币安挂单必须要用websocket才可以,所以我学了学websocket
#但是,学的没有特别明白,所以在创建套接字的时候,用了很多的方法,但是都没有成功,我查阅了币安社区,发现可能是我梯子的问题
#因为币安给的网址没有成功访问,这程序没能正常调试,里边应该不少逻辑和语法的错误,希望面试官原谅

#自己对量化交易很干兴趣,很希望从事这个行业,希望能与面试官一起共事,下面是我的代码
api_key = "vwE11TOZUCc5IHxXuXnZ4eIrNHLl0Pr2Z5kW9yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCV5UgKJj2OexBlnusCzFBA6txxxrCI5HF7miLiri0DbKssN"
symbol = "ETHUSDT"
start_order_amount = 100.0
max_order_amount = 1000.0
total_order_amount = 50000.0
price_move_limit = 0.1
price_margin_percent = 0.01
cancel_range_percentage=0.001
stop_loss_rate=0.01
buy_orders = []
sell_orders = []


global um_futures_client
global current_price

#止盈
async def stop_profit(current_price):
    account_info = um_futures_client.account(recvWindow=6000)
    positions = account_info['positions'][id]

    for position in positions:
        symbol = position['symbol']
        position_size = float(position['positionAmt'])
        unrealized_profit = float(position['unRealizedProfit'])
        #对于每一个订单,只要盈利1%,那就可以平仓
        if symbol == 'ETHUSDT' and position_size != 0:
            # 计算订单盈利
            profit_percent = (unrealized_profit /
                              (position_size * current_price)) * 100

            if profit_percent >= 1.0 :#止盈
                # 平仓
                if position_size > 0:
                    await um_futures_client.new_order(
                        symbol=symbol,
                        side='SELL',  # 平仓
                        type='MARKET',
                        quantity=abs(position_size)
                    )
                else:
                    await um_futures_client.new_order(
                        symbol=symbol,
                        side='SELL',  # 平仓
                        type='MARKET',
                        quantity=abs(position_size)
                    )

async def stop_loss():
    #注意是全仓亏损,所以这里的计算方式和止盈有所差别
    account_info = um_futures_client.account(recvWindow=6000)#先获取账户信息
    if account_info["totalUnrealizedProfit"]/account_info["totalInitialMargin"]>stop_loss_rate:
        for position in positions:
            if position_size > 0:
                    await um_futures_client.new_order(
                        symbol=symbol,
                        side='SELL',  # 平仓
                        type='MARKET',
                        quantity=abs(position_size)
                    )
                else:
                    await um_futures_client.new_order(
                        symbol=symbol,
                        side='SELL',  # 平仓
                        type='MARKET',
                        quantity=abs(position_size)
                    )



                 
async def place_order(side, price, amount):
    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=amount,
            timeInForce="GTC",
            price=price,
        )
        logging.info(response)
    except ClientError as error:
        logging.error("Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        ))


async def cancel_orders(side, order_id):
    try:
        response = um_futures_client.cancel_order(
            symbol=symbol, orderId=order_id, recvWindow=2000)
        logging.info(response)
    except ClientError as error:
        logging.error("Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        ))


async def conduct_orders():
    while True:
        try:
            scope = current_price * price_margin_percent
            buy_price = current_price - scope
            sell_price = current_price + scope

            # 更新50买单
            for i in range(1, 51):
                order_price = buy_price - (scope * (25 - i) / 25)
                order_amount = start_order_amount + \
                    i * (total_order_amount / 50)
                order_amount = min(order_amount, max_order_amount)
                buy_orders.append((order_price, order_amount))

            # 更新50卖单
            for i in range(1, 51):
                order_price = sell_price + (scope * (i - 25) / 25)
                order_amount = start_order_amount + \
                    (i - 25) * (total_order_amount / 50)
                order_amount = min(order_amount, max_order_amount)
                sell_orders.append((order_price, order_amount))

            # 挂单
            for order in buy_orders + sell_orders:
                # IO等待
                await place_order("BUY" if order in buy_orders else "SELL", order[0], order[1])

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Error conduct_orders: {e}")

async def delete_recent_orders():
    while True:
        try:
            open_orders = await um_futures_client.get_open_orders("symbol",recvWindow=100)
            if len(open_orders) > 0:
                min_price = min(float(order["price"]) for order in open_orders)
                max_price = max(float(order["price"]) for order in open_orders)
                if max_price-min_price >= current_price*cancel_range_percentage:
                    # 撤销撤销千分之一范围内的订单
                    for order in open_orders:
                        if float(order["price"]) >= min_price and float(order["price"]) <= max_price:
                            # IO等待
                            await cancel_orders(order["side"], order["orderId"])#先撤单
                            await place_order(order["side"],order["price"],order['amount'])#再挂单
                            if max_price-min_price>=0.05*current_price:#我的理解是波动百分之五在万分之五的下面,如果大于百分之五,那么一定大于万分之5行情剧烈波动,假设为百分之五
                                #这时拉远最近的挂单距离
                                if(order["side"]=="buy"):#如果是买单那就假设向上拉百分之10
                                    await place_order(order["side"],order["price"]*1.1,order["amount"])
                                if(order["side"]=="sell"):#如果是卖单,那就假设向下拉百分之10
                                    await place_order(order["side"],order["price"]*0.9,order["amount"])


        except Exception as e:
            print(f"ERROR delete_recent_orders{e}")

        await asynio.sleep(1)


def on_open():
    data = {
        "method": "SUBSCRIBE",
        "params": [
            "ethusdt@aggTrade",
            "ethusdt@depth"
        ],
        "id": 2
    }
    um_futures_client.send(data)


def on_close():
    print('on close')


def message_handler(_, message):
    print(message)


def on_error(error):
    print(f"on error:{error}")

def target1():

    print("线程1运行")
    
    # socket = 'wss://fstream.binance.com/ws'
    # base_url = socket + '/ethusdt@trade'
    # my_client = websocket.WebSocketApp(
    #     socket + '/ethusdt@trade', on_open=on_open, on_message=message_handler, on_close=on_close)

    my_client = UMFuturesWebsocketClient(
        on_open=on_open,
        on_close=on_close,
        on_message=message_handler,
        on_error=on_error
    )  # 这里的url访问不了,我把梯子调成全局也不行
    # 创建异步时间并运行
    # my_client = BinanceWebsocketClient(
    #     base_url, on_open=on_open, on_close=on_close, on_error=on_error)
    task = [conduct_orders(), delete_recent_orders()]
    # 再写一个线程,进行平仓和止损的操作
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(task))py3.5
    asyncio.run(task)  # py3.7


def target2():
    print("线程2运行")
    task = [stop_profit(current_price),stop_loss()]
    asyncio.run(task)


#这里边很多的注释没有删掉,因为对于websocket的创建不太熟悉
def main():
try:
    um_futures_client = UMFutures(key=api_key, secret=api_secret)   
    current_price = um_futures_client.mark_price(symbol=symbol)
    #这里我认为,止盈止损应该贯穿整个市场行情中,如果单线程的话,可能会发生止盈止损不及时的情况所以我用了两个线程,一个线程用来管理订单,一个用来止盈和止损
    t1=Thread(target=target1)
    t2=Thread(target=target2)
    t2.start()
    t1.start()
    #回收两个线程的资源
except Exception as e:
    t1.join()
    t2.join()
    #这里先启动止盈止损的线程,防止出现意外

if __name__ == '__main__':
    main()
