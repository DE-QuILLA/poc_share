from datetime import datetime, timedelta
import os

def get_target_day(date_str=None):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return datetime.utcnow() - timedelta(days=1)

def ensure_dir_exists(path):
    os.makedirs(path, exist_ok=True)