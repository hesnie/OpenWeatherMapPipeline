"""
TODO: describe the DAG
"""

from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from pendulum import datetime
from airflow.models import Variable
import base64
import logging
import requests

# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["Meteomatics"],
)

# Fetch data from the Meteomatics API
def weather_data():
    @task(
        # Dataset outlet for the task
        outlets=["weather_data"]
    )
    def get_weather_data(**context) -> list[dict]:
        """
        Get API data. 
        TODO: describe this function
        """
        # Fetch the API key from Airflow variables
        try:
            API_USER = Variable.get('API_USER', default_var=None)
            API_SECRET = Variable.get('API_SECRET', default_var=None)
        except Exception as e:
            logging.error("Failed to fetch params from Airflow")
            raise

        # Get API token 
        token_url = "https://login.meteomatics.com/api/v1/token"
        credentials = f"{API_USER}:{API_SECRET}"
        credentials.encode('utf-8')

        astro_api_token = requests.get(
            token_url,
            headers={"Authorization": f"Basic {credentials}"})

        # Creat session using the token for requests
        session = requests.session()
        session.headers = {"Authorization": f"Bearer {astro_api_token}"}

        try:
            response = session.get(
                #TODO: use params, this is testing only
                "https://api.meteomatics.com/2018-07-05T00%3A00%3A00Z/t_2m%3AC/postal_DE10117%2Bpostal_CH9014/json/?source=mix-radar&calibrated=true&mask=land&timeout=300&temporal_interpolation=best"
                )
        except Exception as e:
            logging.error("Failed to fetch the data from Meteomatic API")
            raise 

# Instantiate the DAG
weather_data()