use crate::model::orderbook::Orderbook;
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum OrderbookEvent {
    OrderbookReceived((String, Orderbook)),
    OrderbookChangeReceived((String, Orderbook)),
}
