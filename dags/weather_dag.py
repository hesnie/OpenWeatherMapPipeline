"""
Airflow DAG to fetch weather data from the Meteomatics API, save it in Azure Blob Storage, and transform it for further use, saving it in a star schema in Azure SQL.
This DAG is designed to run daily, fetching the latest weather data and processing it for use in analytics or reporting.
"""

from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from airflow.sdk.operators.bash import BashOperator
from airflow.io.path import ObjectStoragePath
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
        import pandas as pd # Used to handle the data returned from the API

        # Setup vars for API call, fetching one days worth of weather data for a specific location, at 1 hour intervals.
        parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms', 'wind_dir_10m:d', 'uv:idx', 'weather_code_1h:idx']
        model = 'mix'
        startdate = dt.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
        enddate = startdate + dt.timedelta(days=1)
        interval = dt.timedelta(hours=1)
        
        # Fetch variables from Airflow
        try:
            API_USER = Variable.get('API_USER')
            API_SECRET = Variable.get('API_SECRET')
        except Exception as e:
            #logging.error("Failed to fetch params from Airflow")
            raise

        # Query the Meteomatics API for station list in Germany with the dataconnector
        df_stations = api.query_station_list(
            username=API_USER, 
            password=API_SECRET, 
            location='germany') # Limit to Germany for the free API

        # Construct and call the API with the dataconnector
        df_weather = api.query_station_timeseries(
            hash_ids=df_stations['hash_id'].tolist()[0:1],  # Limit to one station for the free API
            startdate=startdate, 
            enddate=enddate, 
            interval=interval, 
            parameters=parameters, 
            username=API_USER, 
            password=API_SECRET, 
            model=model)
        
        # Setup the Azure Blob Storage path for saving the data
        # The path is structured to save station data and weather data in separate directories
        base = ObjectStoragePath("abfs://blob-meteomatic", conn_id="az_blob_storage")
        station_path = base / f"stations/station_data_{startdate}-{enddate}.parquet"
        weather_path = base / f"weather/weather_data_{startdate}-{enddate}.parquet"

        # Save the dataframes to Azure Blob Storage in Parquet format
        with station_path.open("w") as file:
            df_stations.to_parquet(file)
            # TODO: Should log the filetransfer to Azure Blob Storage

        with weather_path.open("w") as file:
            df_weather.to_parquet(file)
            # TODO: Should log the filetransfer to Azure Blob Storage

        # Push filepaths into xcom for later tasks to use
        # This allows subsequent tasks in the DAG to access the saved data files
        get_weather_data.xcom_push(key="station_path", value=station_path)
        get_weather_data.xcom_push(key="weather_path", value=weather_path)

    # Call the task to add it to the DAG
    get_weather_data()

    @task(
        # Dataset outlet for the dbt task
        outlets=["weather_data_transformed"]
    )
    def run_dbt_transformations(**context):
        """
        Run dbt transformations to process the raw weather data.
        This function triggers dbt to run the transformations defined in the dbt project,
        which processes the raw weather data into a star schema format.
        """
        # Define the dbt command to run the transformations
        dbt_command = "dbt run --profiles-dir /opt/airflow/dags/dbt/profiles --project-dir /opt/airflow/dags/dbt/open_weather_map"

        # Use BashOperator to execute the dbt command
        BashOperator(
            task_id="run_dbt_transformations",
            bash_command=dbt_command,
            dag=context['dag'],
        ).execute(context)

    # Call the task to add it to the DAG
    run_dbt_transformations()

# Instantiate the DAG
weather_data()