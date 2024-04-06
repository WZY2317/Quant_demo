以下是使用Python实现您提出的功能的示例代码。请注意，这只是一个基本的框架，您可能需要根据实际需求和环境进行适当的修改和扩展。此代码依赖于`python-binance`库和`asyncio`库。

```python
import asyncio
from binance import AsyncClient, BinanceSocketManager

# 设置币安 API 的密钥
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# 设置交易对和参数
symbol = 'ETHUSDT'  # 交易对
spread_percentage = 0.1  # 价格上下距离的百分比
max_order_quantity = 1000  # 最大订单量（USDT）
initial_order_quantity = 100  # 初始订单量（USDT）
total_order_quantity = 50000  # 订单总量（USDT）
profit_percentage = 0.01  # 获利百分比
stop_loss_percentage = 0.01  # 止损百分比

# 创建异步客户端和Socket管理器
client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
bm = BinanceSocketManager(client)

# 定义订单管理类
class OrderManager:
    def __init__(self):
        self.orders = []

    async def place_orders(self):
        # 获取最新盘口数据
        ticker = await client.get_ticker(symbol=symbol)
        price = float(ticker['lastPrice'])
        buy_price = price - (price * spread_percentage)
        sell_price = price + (price * spread_percentage)

        # 计算买卖订单数量
        buy_quantity = min(initial_order_quantity, max_order_quantity)
        sell_quantity = min(initial_order_quantity, max_order_quantity)

        # 挂买单和卖单
        for i in range(1, 51):  # 上下50个订单
            if i <= 25:
                order_price = buy_price - (buy_price * (25 - i) * spread_percentage)
                order_quantity = buy_quantity + i * (total_order_quantity / 50)
                order_side = 'BUY'
            else:
                order_price = sell_price + (sell_price * (i - 25) * spread_percentage)
                order_quantity = sell_quantity + (i - 25) * (total_order_quantity / 50)
                order_side = 'SELL'

            # 下单操作，待实现

            # 将订单添加到订单列表
            self.orders.append({'side': order_side, 'price': order_price, 'quantity': order_quantity})

    async def cancel_orders(self):
        # 撤销最近千1范围的订单
        # 撤销订单操作，待实现

        # 清空订单列表
        self.orders = []

    async def manage_orders(self):
        while True:
            await self.place_orders()
            await asyncio.sleep(30)  # 每30秒挂一次订单

            # 检查价格波动
            # 若价格波动万5，执行撤单操作和重新挂单操作，待实现

            # 检查订单获利
            # 若订单获利1%，执行平仓操作，待实现

            # 执行止损操作
            # 若全仓亏损1%，执行止损操作，待实现

# 创建订单管理器
order_manager = OrderManager()

# 异步处理函数
async def process_message(message):
    # 处理行情数据，待实现

# 订阅行情数据
async def subscribe_ticker():
    async with bm.ticker_socket(symbol=symbol, callback=process_message):
        while True:
            await asyncio.sleep(1)

# 启动事件循环
loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(subscribe_ticker()),
    loop.create_task(order_manager.manage_orders())
]
loop.run_until_complete(asyncio.wait(tasks))
```

请注意，上述代码中标记为"待实现"的部分需要根据具体的需求和情况进行具体的实现。对于下单、撤销订单、平仓等操作，您需要使用币安提供的相应交易接口进行实际操作。此外，您还需要根据需要添加适当的错误处理、日志记录和其他辅助功能来完善策略的实现。

注意：上述示例代码仅提供了一个基本框架，并且其中的下单、撤销订单、平仓等操作的实现部分需要您根据币安提供的具体交易接口进行编写。此外，代码中的风控和止损逻辑也需要根据您的具体需求进行进一步补充和细化。

在实际使用中，建议您通过测试环境或模拟交易环境进行策略的验证和优化，确保策略的正确性和稳定性。同时，请留意并遵守币安交易所的相关规定、限制和风险提示，避免潜在的风险和损失。