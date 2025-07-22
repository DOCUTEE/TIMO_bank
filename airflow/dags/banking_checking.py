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

def log_postgres_version():
    hook = PostgresHook(postgres_conn_id="postgres_default")
    result = hook.get_first("SELECT version();")
    print("✅ Postgres Version:", result[0])

with DAG(
    dag_id='banking_checking',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run banking checking pipeline',
    tags=['docker', 'banking', 'checking'],
) as dag:

    today = date.today().strftime("%Y-%m-%d")

    start_banking_checking = BashOperator(
        task_id='start_banking_checking',
        bash_command=f'echo "Starting banking checking pipeline {today}"'
    )

    run_select = PostgresOperator(
        task_id="select_version",
        postgres_conn_id="postgres_default",
        sql="SELECT version();"
    )

    print_version = PythonOperator(
        task_id="print_version_result",
        python_callable=log_postgres_version
    )

    ssh_run_script = SSHOperator(
        task_id="run_script_over_ssh",
        ssh_conn_id="ssh_python_service",
        command="python /app/generate_data.py",
        do_xcom_push=True
    )   

    start_banking_checking >> run_select >> print_version
