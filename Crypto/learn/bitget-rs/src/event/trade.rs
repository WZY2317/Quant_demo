use crate::model::trade::TradeInfo;
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum TradeEvent {
    TradeOpen(TradeInfo),
    TradeMatch(TradeInfo),
    TradeFilled(TradeInfo),
    TradeCanceled(TradeInfo),
}
