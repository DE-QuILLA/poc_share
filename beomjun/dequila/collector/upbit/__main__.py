import argparse
from .fetcher import fetch_yesterday_data
from .utils import get_target_day, ensure_dir_exists
from .logger import setup_logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="수집할 날짜 (YYYY-MM-DD)", default=None)
    parser.add_argument("--save_dir", type=str, default="./data/upbit")
    parser.add_argument("--log_path", type=str, default=None)
    args = parser.parse_args()

    setup_logger(args.log_path)

    # 순서대로 비트코인, 이더리움, 도지코인, 솔라나
    markets = ["KRW-BTC", "KRW-ETH", "KRW-DOGE", "KRW-SOL"]
    save_dir = args.save_dir
    target_day = get_target_day(args.date)

    for market in markets:
        fetch_yesterday_data(market=market, save_dir=save_dir, target_day=target_day)