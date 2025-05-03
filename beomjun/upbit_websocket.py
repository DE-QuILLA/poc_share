import aiohttp
import asyncio
import json
import time
from datetime import datetime

async def upbit_websocket():
    url = "wss://api.upbit.com/websocket/v1"
    markets = ["KRW-BTC", "KRW-ETH", "KRW-DOGE", "KRW-SOL"]

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            subscribe_fmt = [
                {"ticket": "unique_ticket"},
                {
                    "type": "ticker",
                    "codes": markets,
                    "isOnlyRealtime": True
                }
            ]
            await ws.send_str(json.dumps(subscribe_fmt))

            data_store = {}
            last_minute = None

            while True:
                msg = await ws.receive()

                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = json.loads(msg.data.decode('utf-8'))
                    code = data['code']
                    price = data['trade_price']
                    volume = data['acc_trade_volume_24h']
                    data_store[code] = {
                        "price": price,
                        "volume": volume,
                        "timestamp": data['timestamp']
                    }

                # 1분마다 저장됨
                now = datetime.now()
                current_minute = now.strftime("%Y%m%d_%H%M")
                if current_minute != last_minute:
                    if data_store:
                        filename = f"prices_{current_minute}.json"
                        with open(filename, "w", encoding="utf-8") as f:
                            json.dump(data_store, f, indent=2, ensure_ascii=False)
                        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] save completed → {filename}")
                    last_minute = current_minute

                await asyncio.sleep(0.5)

asyncio.run(upbit_websocket())
