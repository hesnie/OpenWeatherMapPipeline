"""
Airflow DAG to fetch weather data from the Meteomatics API, save it in Azure Blob Storage, and transform it for further use, saving it in a star schema in Azure SQL.
This DAG is designed to run daily, fetching the latest weather data and processing it for use in analytics or reporting.
"""

from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from airflow.sdk.operators.bash import BashOperator
from pendulum import datetime
from airflow.sdk import Variable
#import logging #TODO: setup azure blob storage for log storage
import datetime as dt
import meteomatics.api as api

# Define the basic parameters of the DAG
@dag(
    start_date=dt(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Henrik S Nielsen", "retries": 2 },
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
        Fetches weather data from the Meteomatics API for a specific location and time range.
        This function queries the API for temperature, UV index, precipitation, and wind speed data at a specified location
        """
        # Setup vars for API call
        coordinates = [(47.11, 11.47)]
        parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms', 'wind_dir_10m:d', 'uv:idx']
        model = 'mix'
        startdate = dt.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
        enddate = startdate + dt.timedelta(days=1)
        interval = dt.timedelta(hours=1)
        
        # Fetch the API key from Airflow variables
        try:
            API_USER = Variable.get('API_USER')
            API_SECRET = Variable.get('API_SECRET')
        except Exception as e:
            #logging.error("Failed to fetch params from Airflow")
            raise

        # Query the Meteomatics API for station list in Germany
        df_stations = api.query_station_list(
            API_USER, 
            API_SECRET, 
            location='germany')
                

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
    def save_raw_weather_data(**context):
        """
        Save raw weather data to Azure blob storage
        This function saves the raw weather data fetched from the Meteomatics API to Azure Blob Storage.
        The data is saved in a CSV format, which can be used for further processing or analysis.
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
    save_raw_weather_data()

    @task(
        # Dataset outlet for the dbt task
        outlets=["weather_data_transformed"]
    )
    def transform_and_save_weather_data(**context):
        """
        Transform raw weather data to the needed data structures, and saves them in Azure SQL
        This function transforms the raw weather data into a star schema format suitable for analytics and reporting.
        The transformed data is then saved in Azure SQL, making it accessible for further analysis or reporting.
        """

    # Call the task to add it to the DAG
    transform_and_save_weather_data()

# Instantiate the DAG
weather_data()