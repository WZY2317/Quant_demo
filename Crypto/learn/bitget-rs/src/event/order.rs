use crate::model::order::LimitOrder;
pub enum OrderEvent {
    GetAllOrders,
    CancelOrder(LimitOrder),
    CancelAllOrders,
    PlaceLimitOrder(LimitOrder),
    PlaceBorrowOrder(LimitOrder),
}
