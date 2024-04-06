import asyncio
import math
import logging
from binance.um_futures import UMFutures as Client
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance import DepthCacheManager
from binance.error import ClientError
config_logging(logging, logging.DEBUG)

api_key = "vwE11TOZUCc5IHxXuXu0nZ4eIrNHLl0Pr2Z5kWw59yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCpnV5UgKJj2OexBlnusCzFBA6txxxrCbyI5HF7miLiri0DbKssN"
symbol = "ETHUSDT"
start_order_amount = 100.0
max_order_amount = 1000.0
total_order_amount = 50000.0
price_move_limit = 0.1
profit_percent = 0.01
stop_loss_rate = 0.01
price_margin_percent = 0.01
delete_range_percent = 0.001
buy_orders = []
sell_orders = []
last_price = None


def message_handler(_, message):
    print(message)


async def place_order(side, price, amount):
    try:
        client = Client(api_key, api_secret,
                        base_url="https://dapi.binance.com")
        response = client.new_order(
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
        client = Client(api_key, api_secret,
                        base_url="https://dapi.binance.com")
        response = client.cancel_order(
            symbol=symbol, orderId=order_id, recvWindow=2000)
        logging.info(response)
    except ClientError as error:
        logging.error("Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        ))


async def conduct_orders():
    while True:
        try:
            scope = last_price * price_margin_percent
            buy_price = last_price - scope
            sell_price = last_price + scope

            # 更新买单
            for i in range(1, 51):
                order_price = buy_price - (scope * (25 - i) / 25)
                order_amount = start_order_amount + \
                    i * (total_order_amount / 50)
                order_amount = min(order_amount, max_order_amount)
                buy_orders.append((order_price, order_amount))

            # 更新卖单
            for i in range(1, 51):
                order_price = sell_price + (scope * (i - 25) / 25)
                order_amount = start_order_amount + \
                    (i - 25) * (total_order_amount / 50)
                order_amount = min(order_amount, max_order_amount)
                sell_orders.append((order_price, order_amount))

            # 挂单
            for order in buy_orders + sell_orders:
                await place_order("BUY" if order in buy_orders else "SELL", order[0], order[1])

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Error conduct_orders: {e}")


async def delete_recent_orders():
    while True:
        try:
            my_client = Client()
            open_orders = await my_client.mark_price("symbol")
            if len(open_orders) > 0:
                min_price = min(float(order["price"]) for order in open_orders)
                max_price = max(float(order["price"]) for order in open_orders)

                if max_price-min_price >= last_price*delete_range_percent:
                    # 撤销最近范围内的订单
                    for order in open_orders:
                        if float(order["price"]) >= min_price and float(order["price"]) <= max_price:
                            await cancel_orders(order["side"], order["orderId"])

        except Exception as e:
            print(f"ERROR delete_recent_orders{e}")

        await asynio.sleep(1)


async def deal_depth_event(depth_cache):
    global last_price
    last_price = depth_cache.get_last_bid_price()


async def main():
    # 创建套接字管理器
    my_client = UMFuturesWebsocketClient()
    my_client.start()
    # 深度行情
    depth_cache_manager = DepthCacheManager(symbol=symbol, limit=10)
    depth_cache_manager.start()
    depth_cache_manager.add_callback(deal_depth_event)
    # 创建异步时间并运行
    task = [conduct_orders(), cancel_orders()]
    await asyncio.gather(*task)
    my_client.stop()


asyncio.run(main())
