from bitmart.lib import cloud_consts
from bitmart.lib.cloud_ws_client import CloudWSClient
from bitmart.ws_spot import create_channel, create_spot_subscribe_params


class WSTest(CloudWSClient):

    def on_message(self, message):
        print(f'[ReceiveServerMessage]-------->{message}')


if __name__ == '__main__':
    ws = WSTest(url=cloud_consts.WS_URL)
    ws.set_debug(False)
    channels = [
        # public channel
        create_channel(cloud_consts.WS_PUBLIC_SPOT_TICKER, 'BTC_USDT'),
        create_channel(cloud_consts.WS_PUBLIC_SPOT_KLINE_1M, 'BTC_USDT'),
        create_channel(cloud_consts.WS_PUBLIC_SPOT_DEPTH5, 'BTC_USDT')

        # or  public channel
        # "spot/ticker:BTC_USDT",
        # "spot/kline1m:BTC_USDT",
        # "spot/depth5:BTC_USDT"
    ]

    ws.spot_subscribe_without_login(create_spot_subscribe_params(channels))
