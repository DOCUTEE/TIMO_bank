from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, date
from airflow.providers.ssh.operators.ssh import SSHOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='banking_checking',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run banking checking pipeline',
    tags=['banking', 'checking'],
) as dag:

    today = date.today().strftime("%Y-%m-%d")

    start_banking_checking = BashOperator(
        task_id='start_banking_checking',
        bash_command=f'echo "Starting banking checking pipeline {today}"'
    )
    generate_data_checking = SSHOperator(
        task_id="generate_data_checking",
        ssh_conn_id="ssh_python_service",
        command="python /app/generate_data.py",
        do_xcom_push=True
    )   
    data_quality_checking = SSHOperator(
        task_id="data_quality_checking",
        ssh_conn_id="ssh_python_service",
        command="python /app/data_quality_standards.py",
        do_xcom_push=True
    ) 

    start_banking_checking >> generate_data_checking >> data_quality_checking