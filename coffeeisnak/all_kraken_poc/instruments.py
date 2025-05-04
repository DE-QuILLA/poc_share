from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 5. Instruments 웹소켓 응답 (활성화 코인 및 거래 방법 등 메타데이터)
    url = "wss://ws.kraken.com/v2"
    channel = "instrument"
    # symbol = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    snapshot = True

    subscribe_dict = {
        "method": "subscribe",
        "params": {
            "channel": channel,
            "snapshot": snapshot
        }
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)
    asyncio.run(client.listen())
