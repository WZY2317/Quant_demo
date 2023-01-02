class TradeData:
    symbol:str=""
    datetime:str=""
    direction:str=""
    price:float=0.0
    volume:float=0.0
    size:int=1

    def __init__(self,symbol:str,datetime:str,direction:str,price:float,volume:float,size:int) -> None:
        self.symbol=symbol
        self.datetime=datetime
        self.direction=direction
        self.price=price
        self.volume=volume
        self.size=size

    def calculate_trading_value(self):
        value=self.price*self.volume*self.size
        return value
    
    def to_str(self)->str:
        text=f"{self.symbol},{self.direction},{self.datetime},{self.volume}手@{self.price}"
        return text

class StockTraceData(TradeData):
   

    def calculate_cash_change(self, size: int):
        value=self.price*self.volume*size
        return value


stock_trade=StockTraceData(
    "60036","20200916 9:30:05","买入",40.0,100.0,1
)

class FuturesTradeData(TradeData):
     margin_rate=0.0
     def __init__(self, symbol: str, datetime: str, direction: str, price: float, volume: float, size: int,margin_rate:float) -> None:
         super().__init__(symbol, datetime, direction, price, volume, size)
         self.margin_rate=margin_rate

future_Trade=FuturesTradeData(
    "TF2010","20200916","买入",4000,1,300,0.15
)


print(stock_trade.to_str())
print("期货成交的现金变化为",future_Trade.calculate_trading_value())

#isinstance 函数

        