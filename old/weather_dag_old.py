from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from extract_weather import extract_weather_data

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='weather_pipeline',
    default_args=default_args,
    description='Pipeline for extracting and transforming OpenWeatherMap data',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_weather_data,
        provide_context=True,
    )

    transform = BashOperator(
        task_id='transform_data_dbt',
        bash_command='cd /opt/airflow/dbt && dbt run',
    )

    test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test',
    )

    extract >> transform >> test