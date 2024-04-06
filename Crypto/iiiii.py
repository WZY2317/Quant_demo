import websocket


async def main():
    wss_url = 'wss://fstream.binance.com'
    ws = websocket.WebSocketApp('wss://fstream.binance.com',
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever(ping_interval=15)
