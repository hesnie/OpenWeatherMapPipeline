-- models/mart/dim_date.sql
/*
This model creates a date dimension table for the Open Weather Map project.
It uses the dbt_date package to generate a date dimension from 1990-01-01 to 2050-12-31.
The date dimension can be used for time-based analysis in the Open Weather Map project.
*/
{{ config(
    alias='dim_date',
    materialized='table',
    schema='open_weather_map'
) }}

{% set date_dimension = dbt_date.get_date_dimension("1990-01-01", "2050-12-31") %}

{{ date_dimension }}