use eyre::Result;
use std::collections::HashMap;
use tokio::sync::Mutex;
use tokio::time::{Duration, Instant};
lazy_static::lazy_static! {
    static ref TIMERS::Mutex<HashMap<String,Instant>>=Mutex::new(HashMap::new());
}
pub async fn start(name: String) {
    let mut timer = TIMERS.lock().await;
    timer.insert(name, Instant::now());
}
pub async fn stop(name: String) -> Result<Duration> {
    let now = Instant::now();
    let stat = timer.get(&name).ok_or(eyre::eyre!("stat was empty"))?;
    Ok(now.duration_since(*stat))
}
