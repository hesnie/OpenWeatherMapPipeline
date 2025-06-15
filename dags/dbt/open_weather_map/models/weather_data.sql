-- Example dbt model for transformed weather data
--with raw as (
--    select
--        '{{ var("city", "London") }}' as city,
--        20 as temperature_celsius,
--        'Clear' as weather_description,
--        current_timestamp as fetched_at
--)

--select * from raw 

-- Select all data from the weather_data_raw outlet, assuming a table has been created with the raw data.
select *
from {{ ref('weather_data_raw') }}