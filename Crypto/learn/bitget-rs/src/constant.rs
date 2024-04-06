pub enum CONSTS {
    API_URL,
    CONTRACT_WS_URL,
}
pub enum REQUESTTYPE {
    GET,
    POST,
}
pub enum PASSWORD {
    APIKEY,
    APISERCET,
    PASSPHRASE,
}
impl PASSWORD {
    pub const APIKEY: &'static str = "bg_16133b342bfcc121556b688e670d5f56";
    pub const APISERCET: &'static str =
        "cab04616e4db4e431a797ffb2d65ab76fb205256cc0c9e230ac75861f68846d8";
    pub const PASSPHRASE: &'static str = "asdsa87024";
}
impl REQUESTTYPE {
    pub const GET: &'static str = "GET";
    pub const POST: &'static str = "POST";
}
pub trait AsStr {
    fn as_str(&self) -> &'static str;
}
impl CONSTS {
    pub const API_URL: &'static str = "https://api.bitget.com";
    pub const CONTRACT_WS_URL: &'static str = "wss://ws.bitget.com/mix/v1/stream";
}
impl AsStr for CONSTS {
    fn as_str(&self) -> &'static str {
        match self {
            CONSTS::API_URL => CONSTS::API_URL.as_str(),
            CONSTS::CONTRACT_WS_URL => CONSTS::CONTRACT_WS_URL.as_str(),
        }
    }
}
