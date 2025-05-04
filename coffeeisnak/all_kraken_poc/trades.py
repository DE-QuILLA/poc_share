from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 4. Trades 웹소켓 응답 (실제 거래 트랜잭션 데이터)
    url = "wss://ws.kraken.com/v2"
    channel = "trade"
    symbol = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    snapshot = True

    subscribe_dict = {
        "method": "subscribe",
        "params": {
            "channel": channel,
            "symbol": symbol,
            "snapshot": snapshot
        }
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)
    asyncio.run(client.listen())
