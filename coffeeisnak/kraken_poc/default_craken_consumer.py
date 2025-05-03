import websocket, json, time

cnt = 0

def fuck_the_connection(ws: websocket.WebSocketApp) -> None:
    unsubscribe_msg = {
        "method": "unsubscribe",
        "params": {
            "channel": "ticker",
            "symbol": ["BTC/USD", "ETH/USD"]
        },
        "req_id": 2,
    }
    ws.send(json.dumps(unsubscribe_msg))

def on_message(ws: websocket.WebSocketApp, message):
    global cnt
    time.sleep(1)
    cnt += 1
    print("바앋으은 데에이이타: ", message)

    if cnt >= 10:
        fuck_the_connection(ws)
        time.sleep(1.5)
        ws.close()  # (뇌피셜) 이거 안하면 파드 안죽을듯 좀 트리키하게 사용 가능할지도 모름

def on_open(ws):
    subscribe_msg = {
        "method": "subscribe",
        "params": {
            "channel": "ticker",
            "symbol": ["BTC/USD", "MATIC/GBP"],
        },
        "req_id": 2,
    }
    ws.send(json.dumps(subscribe_msg))

url = "wss://ws.kraken.com/v2"
ws = websocket.WebSocketApp(url, on_message=on_message, on_open=on_open)
ws.run_forever()
