-- models/staging/stg_weather_condition.sql
with source as (
    select * from {{ ref('weather_code_information') }}
)

select 
    weather_code as weather_condition_code,
    description,
    additional_information
from source
-- This model creates a staging table for weather condition codes.