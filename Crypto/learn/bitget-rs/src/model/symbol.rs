use ordered_float::OrderedFloat;
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct SymbolInfo {
    pub symbol: String,
    pub base: String,
    pub quote: String,
    pub base_min: OrderedFloat<f64>,
    pub base_increment: OrderedFloat<f64>,
}
