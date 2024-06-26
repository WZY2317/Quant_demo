use crate::model::order::OrderSide;
use ordered_float::OrderedFloat;
use std::cmp::Ordering;
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Default)]
pub struct ActionInfo {
    pub action: OrderSide,
    pub ticker: String,
    pub price: OrderedFloat<f64>,
    pub volume: OrderedFloat<f64>,
}
impl ActionInfo {
    pub fn buy(ticker: String, price: OrderedFloat<f64>, volume: OrderedFloat<f64>) -> ActionInfo {
        ActionInfo {
            action: OrderSide::Buy,
            ticker,
            price,
            volume,
        }
    }
    pub fn sell(ticker: String, price: OrderedFloat<f64>, volume: OrderedFloat<f64>) -> ActionInfo {
        ActionInfo {
            action: OrderSide::Sell,
            ticker,
            price,
            volume,
        }
    }
}
impl std::fmt::Debug for ActionInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "ActionInfo {{ {:?} {} at {} for {}}}",
            self.action,
            self.ticker,
            self.price.into_inner(),
            self.volume.into_inner()
        )
    }
}
pub type ThreeActions = [ActionInfo; 3];
#[derive(Debug, Clone, Default, Eq)]
pub struct TriangularArbitrageChance {
    pub profit: OrderedFloat<f64>,
    pub actions: ThreeActions,
}

impl Ord for TriangularArbitrageChance {
    fn cmp(&self, other: &Self) -> Ordering {
        self.profit.cmp(&other.profit)
    }
}

impl PartialOrd for TriangularArbitrageChance {
    fn partial_cmp(&self, other: &TriangularArbitrageChance) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for TriangularArbitrageChance {
    fn eq(&self, other: &Self) -> bool {
        self.profit == other.profit
    }
}
