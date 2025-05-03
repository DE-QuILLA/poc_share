import requests
import time
import json, os
from pathlib import Path
import shutil


def chart_api_call(tick_type: str, symbol: str, resolution: str):
    url = f"https://futures.kraken.com/api/charts/v1/{tick_type}/{symbol}/{resolution}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def save_to_file(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 저장 완료: {filepath}")

# 각 코인별 spot, futures 심볼 매핑
symbols = {
    "btc": {
        "spot": "PF_XBTUSD",
        "mark": "PI_XBTUSD",
    },
    "eth": {
        "spot": "PF_ETHUSD",
        "mark": "PI_ETHUSD",
    },
    "doge": {
        "spot": "PF_DOGEUSD",
        "mark": "PI_DOGEUSD",
    },
    "sol": {
        "spot": "PF_SOLUSD",
        "mark": "PI_SOLUSD",
    }
}




if __name__ == "__main__":
    # 저장 디렉토리 생성
    data_folder = './kraken_ohlc_data'
    try:
        if os.path.exists(data_folder):
            shutil.rmtree(data_folder)
        os.mkdir(data_folder)
    except Exception as e:
        print("fucking directory error: ", e)

    now = int(time.time())
    one_day_age = now - 60 * 60 * 24

    for coin, names in symbols.items():
        for tick_type, tick_name in names.items():
            res = chart_api_call(tick_type, tick_name, '1m')

            save_path = data_folder + f'/{tick_type}_{coin}.json'
            save_to_file(res, save_path)
