-- models/mart/dim_locations.sql
/*
Create a dimension table for OpenWeatherMap locations.
This model selects relevant fields from the staging locations data, 
including station ID, category, type, WMO ID, alternative IDs, station name, 
location coordinates, elevation, start and end dates, and various distance metrics.
This dimension table can be used for analysis of weather data by location.
*/
select
    station_id_hash,
    station_category,
    station_type,
    wmo_id,
    alternative_ids,
    station_name,
    location_lat_lon,
    elevation,
    start_date,
    end_date,
    horizontal_distance,
    distance,
    vertical_distance,
    effective_distance
from
    {{ ref('stg_locations') }}