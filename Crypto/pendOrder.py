import logging
import time
from websocket import create_connection
from binance.client import Client
import binance
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import json
import random

base = "wss://fstream.binance.com"
api_key = "vwE11TOZUCc5IHxXuXu0nZ4eIrNHLl0Pr2Z5kWw59yDIGm5pK7k6X0DvExohpyZI"
api_secret = "OYLN7mk6iC7ycCpnV5UgKJj2OexBlnusCzFBA6txxxrCbyI5HF7miLiri0DbKssN"
# 必要的api信息
PARAM = {
    "symbol": "ETHUSDT",  # 交易币种
    "priceRange": 0.1,  # 波动范围
    "max_order_volume": 1000,  # 最大订单量
    "inital_order_volume": 100,  # 初始订单量
    "total_order_volume": 50000,  # 订单总量
    "profit_rate": 0.01,  # 获利百分比
    "stop_loss_rate": 0.01  # 止损百分比
}


def message_handler(_, message):
    print(message)


# client = Client(api_key, api_secret)
# futureClient = binance.NewFuturesClient(api_key, api_secret)
my_client = SpotWebsocketStreamClient(on_message=message_handler)
# print(client.ping())  # 测试是否成功连接
