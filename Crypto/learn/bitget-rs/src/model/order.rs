use std::{default, str::FromStr, string};

use eyre::Ok;
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Default, Copy)]
pub enum OrderSide {
    #[default]
    Sell,
    Buy,
}
impl AsRef<str> for OrderSide {
    fn as_ref(&self) -> &str {
        match self {
            OrderSide::Buy => "buy",
            OrderSide::Sell => "sell",
        }
    }
}
impl ToString for OrderSide {
    fn to_string(&self) -> String {
        self.as_ref().to_string()
    }
}
impl FromStr for OrderSide {
    type Err = eyre::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "buy" => Ok(OrderSide::Buy),
            "sell" => Ok(OrderSide::Sell),
            unknown => eyre::bail!("unknown side: {unknown}"),
        }
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Default)]
// Market selector, market set to limit order for security
pub enum OrderType {
    #[default]
    Limit,
    Market,
}
impl FromStr for OrderType {
    type Err = eyre::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "limit" => Ok(OrderType::Limit),
            "maket" => Ok(OrderType::Market),
            unknown => eyre::bail!("unknown ordertype {unknown}"),
        }
    }
}
pub trait Order {
    fn id(&self) -> String;
    fn side(&self) -> OrderSide;
    fn symbol(&self) -> String;
    fn amount(&self) -> String;
    fn order_type(&self) -> OrderType;
}
#[derive(Debug, Clone)]
pub struct MarketOrder {
    id: String,
    order_type: OrderType,
    side: OrderSide,
    symbol: String,
    amount: String,
}

impl Order for MarketOrder {
    fn id(&self) -> String {
        self.id.clone()
    }
    fn order_type(&self) -> OrderType {
        self.order_type
    }
    fn side(&self) -> OrderSide {
        self.side
    }
    fn symbol(&self) -> String {
        self.symbol.clone()
    }
    fn amount(&self) -> String {
        self.amount.clone()
    }
}
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct LimitOrder {
    pub id: String,
    pub order_type: OrderType,
    pub side: OrderSide,
    pub symbol: String,
    pub amount: String,
    pub price: String,
}
impl Order for LimitOrder {
    fn id(&self) -> String {
        self.id.clone()
    }
    fn order_type(&self) -> OrderType {
        self.order_type
    }
    fn side(&self) -> OrderSide {
        self.side
    }
    fn symbol(&self) -> String {
        self.symbol.clone()
    }
    fn amount(&self) -> String {
        self.amount.clone()
    }
}
impl LimitOrder {
    pub fn price(&self) -> String {
        self.price.clone()
    }
}
