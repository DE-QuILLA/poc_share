from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 1. Ticker Lv 1 웹소켓 응답 (거래쌍 별 가격 변동 정보)
    url = "wss://ws.kraken.com/v2"
    channel = "ticker"
    symbol = ["BTC/USD", "ETH/USD", "DOGE/USD", "SOL/USD"]
    event_trigger = "trades"
    snapshot = True

    subscribe_dict = {
        "method": "subscribe",
        "params": {
            "channel": channel,
            "symbol": symbol,
            "event_trigger": event_trigger,
            "snapshot": snapshot
        }
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)

    asyncio.run(client.listen())
