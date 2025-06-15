-- models/mart/fact_weather.sql
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