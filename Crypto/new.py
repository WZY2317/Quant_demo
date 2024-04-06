import time
from binance.client import Client
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
import asyncio

PARAM = {
    "symbol": "ETHUSDT",  # 交易币种
    "priceRange": 0.1,  # 波动范围
    "max_order_volume": 1000,  # 最大订单量
    "inital_order_volume": 100,  # 初始订单量
    "total_order_volume": 50000,  # 订单总量
    "profit_rate": 0.01,  # 获利百分比
    "stop_loss_rate": 0.01,  # 止损百分比
    "spread_percentage": 0.1
}
api_key = "vwE11TOZUCc5IHxXuXu0nZ4eIrNHLl0Pr2Z5kWw59yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCpnV5UgKJj2OexBlnusCzFBA6txxxrCbyI5HF7miLiri0DbKssN"

client = Client(api_key=api_key, api_secret=api_secret)


def message_handler(message):
    print(message)


my_client = UMFuturesWebsocketClient(on_message=message_handler)
#这里的stream_url无法访问,可能是网址有问题,或者是代理(梯子的问题)


class orderConductor:
    def __init__(self):
        self.orders = []

    async def place_orders(self):
        mark_price = await my_client.mark_price(symbol=PARAM["symbol"])
        price = float(mark_price)
        buy_price = price - (price * PARAM["spread_percentage"])
        sell_price = price + (price * PARAM["spread_percentage"])
        buy_volume = min(PARAM["initial_order_volume"],
                         PARAM["max_order_volume"])
        sell_volume = min(PARAM["initial_order_volume"],
                          PARAM["max_order_volume"])
        for i in range(1, 51):
            if i <= 25:
                order_price = buy_price -
                    (buy_price * (25 - i) * PARAM["spread_percentage"])
                order_quantity = PARAM["inital_order_volume"] +
                    i * (PARAM["total_order_volume"] / 50)
                order_side = 'BUY'
            else:
                order_price = sell_price +
                    (sell_price * (i - 25) * PARAM["spread_percentage"])
                order_quantity = PARAM["inital_order_volume"] +
                    (i - 25) * (PARAM["total_order_volume"] / 50)
                order_side = 'SELL'
            self.orders.append(
                {'side': order_side, 'price': order_price, 'quantity': order_quantity})

    async def recall_orders(self):
        self.orders = []

    async def conduct_orders(self):
        while True:
            await self.place_orders()
            for order in self.orders:
                # 执行订单下单操作
                print(order)
            await asyncio.sleep(30)


order_conductor = orderConductor()


async def process_message(message):
    # 处理行情数据
    pass


async def acquire_ticker():
    async with my_client.ticker_socket(symbol=PARAM["symbol"], callback=process_message):
        while True:
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(acquire_ticker()),
    loop.create_task(order_conductor.conduct_orders())
]
loop.run_until_complete(asyncio.wait(tasks))
