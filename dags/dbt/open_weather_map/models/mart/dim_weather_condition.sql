-- models/mart/dim_weather_condition.sql
select
    weather_condition_code,
    description,
    additional_information
from
    {{ ref('stg_weather_condition') }}