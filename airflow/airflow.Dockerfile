FROM apache/airflow:2.8.1

USER airflow

# Install the provider as airflow user (the correct way)
RUN pip install --no-cache-dir apache-airflow-providers-postgres==5.10.0

USER root

COPY ./config/airflow.cfg /opt/airflow/airflow.cfg

USER airflow
