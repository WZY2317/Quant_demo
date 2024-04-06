import asyncio
import math
from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
from binance.exceptions import BinanceAPIException
from binance.enums import *

# Binance API认证信息
api_key = "vwE11TOZUCc5IHxXuXu0nZ4eIrNHLl0Pr2Z5kWw59yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCpnV5UgKJj2OexBlnusCzFBA6txxxrCbyI5HF7miLiri0DbKssN"

# 交易对
symbol = "ethusdt"

# 订单参数
initial_order_quantity = 100.0  # 初始订单量
max_order_quantity = 1000.0  # 最大订单量
total_order_quantity = 50000.0  # 订单总量
price_range_percentage = 0.1  # 波动范围百分比
profit_rate = 0.01  # 获利百分比
stop_loss_rate = 0.01  # 止损百分比
spread_percentage = 0.01  # 挂单价差百分比
cancel_range_percentage = 0.001  # 撤单范围百分比

# 全局变量
buy_orders = []
sell_orders = []
last_price = None


async def place_order(side, price, quantity):
    try:
        client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
        order = await client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price
        )
        print(f"Placed order: {order}")
        await client.close_connection()
    except BinanceAPIException as e:
        print(f"Failed to place order: {e}")


async def cancel_order(side, order_id):
    try:
        client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
        result = await client.futures_cancel_order(
            symbol=symbol,
            side=side,
            orderId=order_id
        )
        print(f"Cancelled order: {result}")
        await client.close_connection()
    except BinanceAPIException as e:
        print(f"Failed to cancel order: {e}")


async def manage_orders():
    while True:
        try:
            spread = last_price * price_range_percentage
            buy_price = last_price - spread
            sell_price = last_price + spread

            # 更新买单
            for i in range(1, 51):
                order_price = buy_price - (spread * (25 - i) / 25)
                order_quantity = initial_order_quantity + \
                    i * (total_order_quantity / 50)
                order_quantity = min(order_quantity, max_order_quantity)
                buy_orders.append((order_price, order_quantity))

            # 更新卖单
            for i in range(1, 51):
                order_price = sell_price + (spread * (i - 25) / 25)
                order_quantity = initial_order_quantity + \
                    (i - 25) * (total_order_quantity / 50)
                order_quantity = min(order_quantity, max_order_quantity)
                sell_orders.append((order_price, order_quantity))

            # 挂单
            for order in buy_orders + sell_orders:
                await place_order("BUY" if order in buy_orders else "SELL", order[0], order[1])

            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in manage_orders: {e}")


async def cancel_recent_orders():
    while True:
        try:
            open_orders = await client.futures_get_open_orders(symbol=symbol)
            if len(open_orders) > 0:
                min_price = min(float(order["price"]) for order in open_orders)
                max_price = max(float(order["price"]) for order in open_orders)

                if max_price - min_price >= last_price * cancel_range_percentage:
                    # 撤销最近范围内的订单
                    for order in open_orders:
                        if float(order["price"]) >= min_price and float(order["price"]) <= max_price:
                            await cancel_order(order["side"], order["orderId"])
        except Exception as e:
            print(f"Error in cancel_recent_orders: {e}")

        await asyncio.sleep(1)


async def process_depth_event(depth_cache):
    global last_price
    last_price = depth_cache.get_last_bid_price()


async def main():
    # 创建BinanceSocketManager
    bm = BinanceSocketManager(await AsyncClient.create(api_key=api_key, api_secret=api_secret))

    # 订阅深度行情
    depth_cache_manager = DepthCacheManager(symbol=symbol, limit=10)
    depth_cache_manager.start()

    # 订阅深度行情事件
    depth_cache_manager.add_callback(process_depth_event)

    # 创建任务并运行
    tasks = [manage_orders(), cancel_recent_orders()]
    await asyncio.gather(*tasks)

    # 关闭BinanceSocketManager
    bm.stop_socket(depth_cache_manager)

# 运行主函数
asyncio.run(main())
