use reqwest::header::HeaderMap;
use reqwest::Client;
use std::collections::{hash_map, HashMap};
use std::ptr::metadata;
use std::string;

use crate::constant::{self, AsStr, PASSWORD, REQUESTTYPE};
use crate::strings::parse_params_to_str;
use base64::prelude::*;
use hmac::{Hmac, Mac};
use sha2::Sha256;
use tungstenite;
pub struct ClientBitget {
    api_key: String,
    api_secret: String,
    passparse: String,
}

impl ClientBitget {
    pub fn new() -> ClientBitget {
        ClientBitget {
            api_key: PASSWORD::APIKEY,
            api_secret: PASSWORD::APISERCET,
            passparse: PASSWORD::PASSPHRASE,
        }
    }
    pub fn login(self) {
        let (mut client, response) =
            tungstenite::connect(constant::CONSTS::CONTRACT_WS_URL.as_str()).unwrap();
        println!("Connected to the server");
        println!("Response HTTP code: {}", response.status());
        println!("Response contains the following headers:");
        println!("{:?}", response.headers());
        let auth_msg = self.generate_login_msg();
        println!("{auth_msg}");
        // let auth_msg = BitgetAuth::ws_auth(options).unwrap();
        // println!("{auth_msg}");
        client.send(auth_msg.into()).unwrap();
        let auth_resp = client.read().unwrap();
        println!("{}", auth_resp);
    }
    pub fn generate_login_msg(self) -> String {
        let secret_key = self.api_secret;
        type HmacSha256 = Hmac<Sha256>;
        let _timestamp = format!("{}", chrono::Utc::now().timestamp_millis() / 1000);
        let method = String::from("GET");
        let request_path = String::from("/user/verify");
        let message = format!("{}{}{}", _timestamp, method, request_path);
        let mut key = HmacSha256::new_from_slice(secret_key.as_bytes())
            .expect("HMAC can take key of any size");
        key.update(message.as_bytes());
        let signature = BASE64_STANDARD.encode(key.finalize().into_bytes());
        let api_key = self.api_key;
        let _passphrase = self.passparse;
        let msg = format!(
            r#"{{"op": "login","args": [{{"api_key": "{key}","passphrase": "{passphrase}","timestamp": "{timestamp}","sign": "{signature}"}}]}}"#,
            key = api_key,
            passphrase = _passphrase,
            timestamp = _timestamp,
            signature = signature
        );
        msg
    }
    pub fn get_signture(self) -> String {
        let secret_key = self.api_secret;
        type HmacSha256 = Hmac<Sha256>;
        let _timestamp = format!("{}", chrono::Utc::now().timestamp_millis() / 1000);
        let method = String::from("GET");
        let request_path = String::from("/user/verify");
        let message = format!("{}{}{}", _timestamp, method, request_path);
        let mut key = HmacSha256::new_from_slice(secret_key.as_bytes())
            .expect("HMAC can take key of any size");
        key.update(message.as_bytes());
        let signature = BASE64_STANDARD.encode(key.finalize().into_bytes());
        signature
    }

    pub fn close_all_positions(self, product_type: String) -> Result<(), reqwest::Error> {
        let request_path = "/api/mix/v1/order/close-all-positions";
        let url = constant::CONSTS::API_URL.to_owned() + request_path;
        let signature = self.get_signature();

        let mut params = HashMap::new();
        params.insert("productType", &product_type);
        let timestamp = chrono::Utc::now().timestamp_millis() / 1000;

        let client = Client::new();
        let request = client
            .post(&url)
            .headers(self.get_header(PASSWORD::APIKEY, timestamp, PASSWORD::PASSPHRASE, signature))
            .query(&params)
            .build()?;

        let response = client.execute(request)?;
        // Process the response as needed

        Ok(())
    }
    pub fn request(
        self,
        method: REQUESTTYPE,
        mut request_path: String,
        params: HashMap<&str, &str>,
        body: Option<&str>,
    ) -> String {
        if method == REQUESTTYPE::GET {
            request_path = request_path + &parse_params_to_str(&params);
        }
        let url = constant::CONSTS::API_URL + &request_path;
        let sign = self.get_signture();
        let timestamp = chrono::Utc::now().timestamp_millis() / 1000;
        let header = self.get_header(PASSWORD::APIKEY, timestamp, PASSWORD::PASSPHRASE, sign);
        let client = Client::new();
        let mut request_builder = match method {
            REQUESTTYPE::GET => client.get(&url),
            REQUESTTYPE::POST => client.post(&url),
        };
        let request = request_builder
            .headers(header)
            .query(&params)
            .body(body.unwrap_or(""))
            .build()
            .unwrap();

        let response = client.execute(request).unwrap();
        let response_text = response.text().unwrap();
        println!("response: {}", response_text);
        response_text
    }
    pub fn get_header(
        self,
        api_key: PASSWORD,
        timestamp: &str,
        passphrase: PASSWORD,
        sign: String,
    ) -> HashMap<&str, &str> {
        let mut header = HashMap::new();
        header["Content-Type"] = "application/json";
        header["ACCESS-KEY"] = api_key;
        header["ACCESS-PASSPHRASE"] = passphrase;
        header["TIMESTAMP"] = timestamp;
        header["locale"] = "zh-CN";
        header
    }
}
