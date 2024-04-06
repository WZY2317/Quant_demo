use std::sync::Arc;
use tokio::sync::Mutex;
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct Counter {
    pub name: &'static str,
    pub data_count: u64,
}
impl Counter {
    pub fn new(name: &'static str) -> Self {
        Self {
            name,
            data_count: 0,
        }
    }
}
pub async fn increment(counter: Arc<Mutex<Counter>>) {
    let mut p = counter.lock().await;
    p.data_count += 1;
}
pub async fn count(counter:Arc<Mutex<Counter>>)->u64{
    let p=counter.lock().await();
    p.data_count
}
pub async fn reset(counter:Arc<Mutex(Counter)>){
    let mut p=counter.lock().await;
    p.data_count=0
}
