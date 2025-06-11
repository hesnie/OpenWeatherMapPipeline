"""
TODO: describe the DAG
"""

from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from pendulum import datetime
from airflow.sdk import Variable
import logging
import requests
import datetime as dt
import meteomatics.api as api

# Define the basic parameters of the DAG
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Henrik S Nielsen", "retries": 0 }, #TODO: replace with "retries": 2},
    tags=["Meteomatics"],
)

# Fetch data from the Meteomatics API
def weather_data():
    @task(
        # Dataset outlet for the api task
        outlets=["weather_data_raw"]
    )
    def get_weather_data(**context):
        """
        Get API data. 
        TODO: describe this function
        """
        # Setup vars for API call
        coordinates = [(47.11, 11.47)]
        parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms']
        model = 'mix'
        startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        enddate = startdate + dt.timedelta(days=1)
        interval = dt.timedelta(hours=1)
        
        # Fetch the API key from Airflow variables
        try:
            API_USER = Variable.get('API_USER')
            API_SECRET = Variable.get('API_SECRET')
        except Exception as e:
            #logging.error("Failed to fetch params from Airflow")
            raise

        # Construct and call the API with the dataconnector
        df_weather = api.query_time_series(
            coordinates, 
            startdate, 
            enddate, 
            interval, 
            parameters, 
            API_USER, 
            API_SECRET, 
            model=model)

        return df_weather

    # Call the task to add it to the DAG
    get_weather_data()

    @task(
        # Dataset outlet for the dbt task
        outlets=["weather_data_raw"]
    )
    def transform_weather_data(**context):
        """
        """    
        
        # Define paths to dbt project and virtual environment
        PATH_TO_DBT_PROJECT =  "/home/user/dbt_projects/openweathermap_dbt"
        PATH_TO_DBT_VENV = "/home/user/venvs/dbt_env/bin/activate"

        dbt_run = BashOperator(
            task_id="dbt_run",
            bash_command="source $PATH_TO_DBT_VENV && dbt run --models .",
            env={"PATH_TO_DBT_VENV": PATH_TO_DBT_VENV},
            cwd=PATH_TO_DBT_PROJECT,
        )

    # Call the task to add it to the DAG
    transform_weather_data

# Instantiate the DAG
weather_data()