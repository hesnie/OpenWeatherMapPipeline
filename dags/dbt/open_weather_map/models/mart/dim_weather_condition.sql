-- models/mart/dim_weather_condition.sql
/*
Create a dimension table for OpenWeatherMap weather conditions.
This model selects relevant fields from the staging weather condition data, 
including weather condition code, description, and additional information.
This dimension table can be used for analysis of weather data by condition.
*/
select
    weather_condition_code,
    description,
    additional_information
from
    {{ ref('stg_weather_condition') }}