import os
import json
import time
import logging
from datetime import datetime, timedelta
import requests

def get_minute_candles(market="KRW-BTC", to=None, count=200):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    headers = {"Accept": "application/json"}
    params = {"market": market, "to": to, "count": count}

    max_retries = 3
    backoff_seconds = 3

    for attempt in range(1, max_retries + 1):
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logging.warning(f"[{attempt}] Rate limit exceeded (429). Retrying in {backoff_seconds} seconds...")
            time.sleep(backoff_seconds)
        else:
            logging.warning(f"API request failed with status {response.status_code}: {response.text}")
            return []

    logging.error("All retry attempts failed. Giving up the request.")
    return []

def fetch_yesterday_data(market="KRW-BTC", save_dir="./data/upbit", target_day=None):
    # UTC 기준 전날
    if target_day is None:
        target_day = datetime.utcnow() - timedelta(days=1)
    start_time = datetime(target_day.year, target_day.month, target_day.day, 0, 0)

    all_data = []

    for i in range(8):
        to_str = (start_time + timedelta(minutes=200)).strftime("%Y-%m-%dT%H:%M:%S")
        data = get_minute_candles(market=market, to=to_str, count=200)
        if not data:
            logging.warning(f"[{i}] No data returned or API request failed.")
            break

        filtered = [
            d for d in data
            if d["candle_date_time_utc"].startswith(target_day.strftime("%Y-%m-%d"))
        ]
        all_data.extend(filtered)

        last_time = max(
            datetime.strptime(d["candle_date_time_utc"], "%Y-%m-%dT%H:%M:%S") for d in data
        )
        start_time = last_time + timedelta(minutes=1)

        logging.info(
            f"[{i}] Retrieved {len(filtered)} entries | {filtered[-1]['candle_date_time_utc']} to {filtered[0]['candle_date_time_utc']}"
        )

    all_data = sorted(all_data, key=lambda x: x["candle_date_time_utc"])

    expected_times = {
        (datetime(target_day.year, target_day.month, target_day.day) + timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:00")
        for i in range(1440)
    }
    collected_times = {item["candle_date_time_utc"] for item in all_data}
    missing = sorted(expected_times - collected_times)

    if missing:
        logging.warning(f"{len(missing)} missing time points detected.")
        for t in missing[:5]:
            logging.warning(f"Missing: {t}")
        if len(missing) > 5:
            logging.warning("... (more missing entries omitted)")
    else:
        logging.info("All 1-minute candles successfully collected (1440 entries).")

    os.makedirs(f"{save_dir}/{market}", exist_ok=True)
    out_path = f"{save_dir}/{market}/{target_day.strftime('%Y-%m-%d')}.json"
    with open(out_path, "w") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Saved to: {out_path}")
