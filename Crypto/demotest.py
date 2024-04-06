import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import asyncio
from binance import BinaceSocketManager


config_logging(logging, logging.DEBUG)

api_key = "vwE11TOZUCc5IHxXuXu0nZ4eIrNHLl0Pr2Z5kWw59yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCpnV5UgKJj2OexBlnusCzFBA6txxxrCbyI5HF7miLiri0DbKssN"

params = {
    "symbol": "ETHUSDT",  # 交易币种
    "priceRange": 0.1,  # 波动范围
    "max_order_volume": 1000,  # 最大订单量
    "inital_order_volume": 100,  # 初始订单量
    "total_order_volume": 50000,  # 订单总量
    "profit_rate": 0.01,  # 获利百分比
    "stop_loss_rate": 0.01  # 止损百分比
}

client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
# client = await SpotWebsocketStreamClient(on_message=message_handler)
BSM = BinanceSocketManager(client)

# 定义订单类


class Orders:
    def __init__(self) -> None:
        self.Orders = []

    # @asyncio.coroutine
    async def getOrders(self):
        ticker = await client.book_ticker(symbol="ETHUSDT")
        price = float(ticker[''])


# time.sleep(10)
