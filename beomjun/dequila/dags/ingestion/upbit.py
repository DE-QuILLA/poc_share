from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "Beomjun",
    "start_date": datetime(2025, 5, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="upbit_collector_daily",
    default_args=default_args,
    schedule_interval="0 1 * * *",
    catchup=False,
    tags=["upbit", "daily"],
) as dag:

    run_collector = BashOperator(
        task_id="run_upbit_collector",
        bash_command=(
            "PYTHONPATH=/opt/airflow "
            "python -m collector.upbit "
            "--date {{ ds }} "
            "--log_path /opt/airflow/logs/upbit/upbit_{{ ds }}.log "
            "--save_dir /opt/airflow/data/upbit"
        )
    )
