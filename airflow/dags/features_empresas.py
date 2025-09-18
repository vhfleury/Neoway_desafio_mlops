from datetime import datetime, timedelta
from airflow import DAG

from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from spark_processing.features_empresas import run_feature
from connections.cache import check_redis_connection


default_args = {
    "owner": "neoway",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="features_empresas",
    description="empresas, features by city",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    params={
        "csv_path": Param(
            "/opt/airflow/data/features_empresas/raw/novas_empresas.csv",
            type="string",
            description="Absolute path of the CSV inside the Airflow container",
        )
    },

) as dag:

    start = BashOperator(
        task_id="start",
        bash_command='echo "Starting to process company data..."'
    )

    check_redis = PythonOperator(
        task_id="check_redis",
        python_callable=check_redis_connection
    )

    feature = PythonOperator(
        task_id="run_feature",
        python_callable=run_feature,
        op_kwargs={
            "input_path": "{{ dag_run.conf.get('csv_path', params.csv_path) }}",
            "output_dir": "/opt/airflow/data/features_empresas/processed",
            "run_date": "{{ ds }}",
        }
    )

    start >> check_redis >> feature
