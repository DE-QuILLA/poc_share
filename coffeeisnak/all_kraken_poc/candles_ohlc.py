from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 3. Candles (OHLC) 웹소켓 응답 (Open, High, Low, Close 정보 채널)
    url = "wss://ws.kraken.com/v2"
    channel = "ohlc"
    symbol = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    snapshot = True

    subscribe_dict = {
        "method": "subscribe",
        "params": {
            "channel": channel,
            "symbol": symbol,
            "interval": 1,          # 가능한 값: [1, 5, 15, 30, 60, 240, 1440, 10080, 21600] => 분단위
            "snapshot": snapshot  # 커넥션 후 snapshot 요청 여부
        }
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)
    asyncio.run(client.listen())
