from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 2. Book Lv 2 웹소켓 응답 (호가창 실시간 정보)
    url = "wss://ws.kraken.com/v2"
    channel = "book"
    symbol = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    event_trigger = "trades"
    snapshot = True

    subscribe_dict = {
        "method": "subscribe",
        "params": {
            "channel": channel,
            "symbol": symbol,
            "depth": 10,          # 가능한 값: [10, 25, 100, 500, 1000], 기본 10
            "snapshot": snapshot  # 커넥션 후 snapshot 요청 여부
        }
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)

    asyncio.run(client.listen())
