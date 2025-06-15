-- models/staging/stg_weather.sql
/*
Create a staging model for OpenWeatherMap weather data.
This model is used to prepare the data for further transformations and analysis.    
It selects relevant fields from the raw weather data and renames them for clarity.
*/
with source as (
    select * 
    from {{ source('raw_openweathermap' ,'raw_weather') }}
)

select
    'station_id' as station_id_hash,
    'validdate' as valid_date,
    't_2m:C' as temperature_2m_celsius,
    'precip_1h:mm' as precipitation_1h_mm,
    'wind_speed_10m:ms' as wind_speed_10m_ms,
    'wind_dir_10m:d' as wind_direction_10m_degrees,
    'uv:idx' as uv_index,
    'weather_code_1h:idx' as weather_condition_code,
from source