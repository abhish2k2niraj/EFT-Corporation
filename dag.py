from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from transform_load import transform_load

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="daily_transactions_dag",
    default_args=default_args,
    description="Daily transaction processing DAG",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id="transform_and_load",
        python_callable=transform_load
    )

    task1
