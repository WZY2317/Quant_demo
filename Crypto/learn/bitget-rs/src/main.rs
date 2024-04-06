mod api {
    pub mod sdk;
}
mod model {
    pub mod chance;
    pub mod order;
    pub mod orderbook;
    pub mod symbol;
    pub mod trade;
}
use api::sdk;
fn main() {
    let client = sdk::ClientBitget::new();
    //client.login();

    println!("Hello, world!");
}
