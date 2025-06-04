-- Example dbt test: Check temperature is above absolute zero
select *
from {{ ref('weather_data') }}
where temperature_celsius < -273.15