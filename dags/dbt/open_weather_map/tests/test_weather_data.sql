-- Example dbt test: Check temperature is above absolute zero and below boiling point
select *
from {{ ref('fact_weather') }}
where temperature_2m_celsius < -273.15
or temperature_2m_celsius > 100.00