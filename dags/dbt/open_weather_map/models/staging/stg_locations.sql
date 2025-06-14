-- models/staging/stg_locations.sql
/*
Create a staging model for OpenWeatherMap stations data.
This model is used to prepare the data for further transformations and analysis.
It selects relevant fields from the raw stations data and renames them for clarity.
*/
with source as (
    select * 
    from {{ source('raw_openweathermap' ,'raw_stations') }}
)

select
    'ID Hash' as station_id_hash,
    'Station Category' as  station_category,
    'Station Type' as station_type,
    'WMO ID' as  wmo_id,
    'Alternative IDs' as alternative_ids,
    'Name' as station_name,
    'Location Lat,Lon' as location_lat_lon,
    'Elevation' as elevation,
    'Start Date' as start_date,
    'End Date' as end_date,
    'Horizontal' as horizontal_distance,
    'Distance' as distance,
    'Vertical Distance' as vertical_distance,
    'Effective Distance' as effective_distance,
from source