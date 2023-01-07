class TradeData:
    symbol: str = ""
    datetime: str = ""
    direction: str = ""
    price: float = 0.0
    volume: float = 0.0
    size: int = 1

    def __init__(self, symbol: str, datetime: str, direction: str, price: float, volume: float, size: int) -> None:
        self.symbol = symbol
        self.datetime = datetime
        self.direction = direction
        self.price = price
        self.volume = volume
        self.size = size

    def calculate_trading_value(self):
        value = self.price*self.volume*self.size
        return value

    def trade_log(self, strategy_name: str):
        text = f"{strategy_name}成交数据,self.to_str()"
        print(text)

    def to_str(self) -> str:
        text = f"{self.symbol},{self.direction},{self.datetime},{self.volume}手@{self.price}"
        return text


class StockTraceData(TradeData):
    def calculate_cash_change(self, size: int):
        value = self.price*self.volume*size
        return value


class FuturesTradeData(TradeData):
    margin_rate = 0.0

    def __init__(self, symbol: str, datetime: str, direction: str, price: float, volume: float, size: int, margin_rate: float) -> None:
        super().__init__(symbol, datetime, direction, price, volume, size)
        self.margin_rate = margin_rate

    def calculate_cash_change(self, size: int):
        value = self.price*self.volume*size
        return value

    def to_str(self) -> str:
        cash_change = self.calculate_cash_change(3)
        text = f"{self.symbol},{self.direction},{self.datetime},{self.volume}手@{self.price}消耗保证金{cash_change}"
        return text

    def trade_log(self, strategy_name: str):
        return super().trade_log(strategy_name)


def print_strategy_trade_twice(trade: TradeData, strategy_name: str):
    trade.trade_log(strategy_name)
    trade.trade_log(strategy_name)
