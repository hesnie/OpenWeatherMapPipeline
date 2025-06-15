-- models/staging/stg_weather_condition.sql
/*
Create a staging model for OpenWeatherMap weather condition codes.
This model is used to prepare the data for further transformations and analysis.  
It selects relevant fields from the weather code information and renames them for clarity.
*/
with source as (
    select * from {{ ref('weather_code_information') }}
)

select 
    weather_code as weather_condition_code,
    description,
    additional_information
from source
-- This model creates a staging table for weather condition codes.