from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ashok',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['your@email.com']
}

with DAG(
    dag_id='stock_market_pipeline',
    default_args=default_args,
    description='Real-Time Stock Market Data Pipeline',
    schedule_interval='@hourly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['data-engineering', 'stocks', 'delta-lake']
) as dag:

    bronze_task = BashOperator(
        task_id='bronze_ingestion',
        bash_command='spark-submit /opt/pipeline/processing/bronze_ingestion.py'
    )

    silver_task = BashOperator(
        task_id='silver_transform',
        bash_command='spark-submit /opt/pipeline/processing/silver_transform.py'
    )

    gold_task = BashOperator(
        task_id='gold_aggregation',
        bash_command='spark-submit /opt/pipeline/processing/gold_aggregation.py'
    )

    dbt_task = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /opt/pipeline/dbt_models'
    )

    bronze_task >> silver_task >> gold_task >> dbt_task
