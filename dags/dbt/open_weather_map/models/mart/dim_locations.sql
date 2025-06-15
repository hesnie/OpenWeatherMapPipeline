-- models/mart/dim_locations.sql
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