-- models/mart/fact_weather.sql
/*
Create a fact table for OpenWeatherMap weather data.
This model selects relevant fields from the staging weather data,
including station ID, weather condition code, date, temperature, precipitation,
wind speed, wind direction, and UV index.
This fact table can be used for analysis of weather data over time and by location.
It is linked to the dim_locations, dim_date and dim_weather_condition dimensions.
*/
select
    station_id_hash,
    weather_condition_code,
    valid_date as date,
    temperature_2m_celsius,
    precipitation_1h_mm,
    wind_speed_10m_ms,
    wind_direction_10m_degrees,
    uv_index,
from
    {{ ref('stg_weather') }}