import asyncio
import websockets
import json
from datetime import datetime

def save_instrument_snapshot(data, filename=None):
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"./sample_data/instruments_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[✓] Instrument snapshot saved to: {filename}")

async def listen_instruments():
    url = "wss://ws.kraken.com/v2"
    subscribe_msg = {
        "method": "subscribe",
        "params": {
            "channel": "instrument",
            "snapshot": True  # snapshot 수신을 요청
        }
    }

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(subscribe_msg))
        print("[*] Subscribed to instrument channel. Waiting for snapshot...")

        async for message in ws:
            msg = json.loads(message)
            if msg.get("channel") == "instrument" and msg.get("type") == "snapshot":
                save_instrument_snapshot(msg)
                break  # snapshot만 받고 종료하려면 break

if __name__ == "__main__":
    asyncio.run(listen_instruments())
