use std::collections::HashMap;
pub fn symbol_to_string(base: &str, quote: &str) -> String {
    let mut n = String::from(base);
    n.push('_');
    n.push_str(quote);
    n
}
pub fn topic_to_symbol(topic: String) -> Option<String> {
    let n = topic.find(':')? + 1;
    let x = topic.as_str();
    Some(String::from(&x[n..]))
}
pub fn symbol_to_tuple(ticker: &str) -> Option<(&str, &str)> {
    let n = ticker.find('-')?;
    Some(((&ticker[..n]), (&ticker[(n + 1)..])))
}
pub fn split_symbol(symbol: String) -> Option<(String, String)> {
    let delimiter = "-";
    let substrings: Vec<String> = symbol
        .split(delimiter)
        .map(|s| s.trim().to_string())
        .collect();
    Some((substrings[0].to_owned(), substrings[1].to_owned()))
}
// def parse_params_to_str(params):
//     params = [(key, val) for key, val in params.items()]
//     params.sort(key=lambda x: x[0])
//     # from urllib.parse import urlencode
//     # url = '?' +urlencode(params);
//     url = '?' +toQueryWithNoEncode(params);
//     if url == '?':
//         return ''
//     return url
//     # url = '?'
//     # for key, value in params.items():
//     #     url = url + str(key) + '=' + str(value) + '&'
//     #
//     # return url[0:-1]
pub fn parse_params_to_str(params: &HashMap<&str, &str>) -> String {
    let mut params_vec: Vec<(&&str, &&str)> = params.iter().collect();
    params_vec.sort_by_key(|&(key, _)| key);

    let mut query_string = String::from("?");
    for (key, value) in params_vec {
        query_string.push_str(*key);
        query_string.push('=');
        query_string.push_str(*value);
        query_string.push('&');
    }

    if query_string == "?" {
        String::new()
    } else {
        query_string.pop(); // Remove the trailing '&'
        query_string
    }
}
