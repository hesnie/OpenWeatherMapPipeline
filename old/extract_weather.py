import os
import logging
import requests
from airflow.models import Variable

def extract_weather_data(**context):
    api_key = Variable.get('OPENWEATHERMAP_API_KEY', default_var=None)
    city = Variable.get('WEATHER_CITY', default_var='London')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather = response.json()
        # Save or push data for downstream tasks
        context['ti'].xcom_push(key='raw_weather', value=weather)
        logging.info("Weather data extraction successful for city: %s", city)
    except Exception as e:
        logging.error("Failed to extract weather data: %s", str(e))
        raise