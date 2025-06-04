# OpenWeatherMapPipeline
## Overview
This repository contains an Apache Airflow pipeline for fetching weather data from OpenWeatherMap.

## Table of Contents
* Overview
* Features
* Project Structure
* Getting Started
* Configuration
* Usage
* DAG Details
* License

## Features
- Automated data extraction from OpenWeatherMap
- Data transformation/cleaning tasks
- Data loading into TBD
- Error handling and alerting

## Project Structure
Code
├── dags/
│   └── weather_dag.py
├── plugins/
├── requirements.txt
├── README.md
Getting Started
Prerequisites
Python >= 3.x
Apache Airflow >= 2.x
Docker (optional, for containerized deployment)

## Installation
### Clone the repository:

bash
git clone https://github.com/hesnie/OpenWeatherMapPipeline.git
cd OpenWeatherMapPipeline
Install dependencies:

bash
pip install -r requirements.txt
Initialize Airflow:

bash
airflow db init
Configuration
Set your OpenWeatherMap API key and other secrets as Airflow Variables or Connections.
Example .env (if used):
Code
OPENWEATHERMAP_API_KEY=your_api_key
Usage
Start the Airflow webserver and scheduler:
bash
airflow webserver
airflow scheduler
Access the Airflow UI at http://localhost:8080 and enable the DAG.
DAG Details
Task Name	Description
extract_weather_data	Fetches weather data from OpenWeatherMap
transform_data	Cleans and processes raw data
load_to_db	Loads transformed data to the destination

## License
MIT
