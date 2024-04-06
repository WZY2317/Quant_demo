import time
from binance.cm_futures import CMFutures
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

cm_futures_client = CMFutures(key=api_key, secret=api_secret)
# bsm = BinaceSocketManager(cm_futures_client)
# base_url = "fapi.binance.com"
# Get account information
# print(cm_futures_client.account())


def message_handler(message):
    print(message)


# stream_url="wss://fstream.binance.com",这里的url出现了无法访问的问题
my_client = UMFuturesWebsocketClient(on_message=message_handler)
# 这里因为基础网址无法访问,会出现timeout的错误
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.002,
    'price': 59808
}


class orderConductor:
    def __init__(self):
        self.orders = []

    async def place_orders(self):
        # ticker = await my_client.ticker(symbol=PARAM.symbol, type="FULL")
        mark_price = await my_client.mark_price(symbol=PARAM.symbol)
        price = float(price)
        buy_price = price - (price * PARAM.spread_percentage)
        sell_price = price + (price * PARAM.spread_percentage)
        buy_volume = min(PARAM.initial_order_quantity,
                         PARAM.max_order_quantity)
        sell_volume = min(PARAM.initial_order_quantity,
                          PARAM.max_order_quantity)  # 挂买单和卖单
        for i in range(1, 51):  # 上下50个订单
            if i <= 25:
                order_price = buy_price - \
                    (buy_price * (25 - i) * PARAM.spread_percentage)
                order_quantity = PARAM.buy_quantity + \
                    i * (PARAM.total_order_quantity / 50)
                order_side = 'BUY'
            else:
               order_price = sell_price + \
                    (sell_price * (i - 25) * PARAM.spread_percentage)
               order_quantity = PARAM.sell_quantity + \
                    (i - 25) * (PARAM.total_order_quantity / 50)
               order_side = 'SELL'
               self.orders.append({'side': order_side, 'price': order_price, 'quantity': order_quantity})
    async def recall_orders(self):
            # 撤销最近千1范围的订单
            # 撤销订单操作，待实现

            # 清空订单列表
         self.orders = []
    async def conduct_orders(self):
        while True:
            await self.place_orders()
            await asyncio.sleep(30) 


order_conductor=orderConductor()
    async def process_message(message):
        #处理行情数据,还未实现

    #获取行情数据
    async def acqiure_ticker():
        async with my_client.ticker_socket(symbol=PARAM.symbol,callback=process_message):
            while True:
                    await asyncio.sleep(1)
loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(acqiure_ticker()),
    loop.create_task(order_conductor.conduct_orders())
]
loop.run_until_complete(asyncio.wait(tasks))