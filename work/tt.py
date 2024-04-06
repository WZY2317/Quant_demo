import websocket
import json
import zlib


def on_open(ws):
    data = {"op": "subscribe", "args": ["spot/ticker:BTC_USDT"]}
    ws.send(json.dump(data))


def on_error(ws, error):
    print(f"on error={error}")


def on_message(ws, msg):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    inflated = decompress.decompress(msg)
    mg = json.loads(inflated)
    print(mg)


base_url = 'wss://ws-manager-compress.bitmart.com/api?protocol=1.1'

if __name__ == '__main__':
    wss_url = base_url
    ws = websocket.WebSocketApp(
        base_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error
    )

    ws.run_forever(ping_timeout=15)
