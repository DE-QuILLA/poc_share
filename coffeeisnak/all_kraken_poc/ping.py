from kraken_websocket_client import KrakenWebSocketClient
import asyncio

if __name__ == "__main__":
    # 6. Ping 웹소켓 응답
    url = "wss://ws.kraken.com/v2"
    channel = "ping"

    subscribe_dict = {
        "method": "ping",
    }

    client = KrakenWebSocketClient(url, subscribe_dict=subscribe_dict)

    asyncio.run(client.listen())
