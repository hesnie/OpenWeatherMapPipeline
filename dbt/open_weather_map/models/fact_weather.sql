-- Fact Table: Weather Fact
CREATE TABLE IF NOT EXISTS fact_weather (
    weather_id SERIAL PRIMARY KEY,
    date_id DATE NOT NULL REFERENCES dim_date(date_id),
    location_id INTEGER NOT NULL REFERENCES dim_location(location_id),
    condition_id INTEGER NOT NULL REFERENCES dim_weather_condition(condition_id),
    temperature_celsius DECIMAL(5,2) NOT NULL,
    humidity INTEGER NOT NULL,
    pressure INTEGER NOT NULL,
    wind_speed DECIMAL(5,2),
    wind_direction INTEGER,
    fetched_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);