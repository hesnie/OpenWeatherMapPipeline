-- Dimension: Weather Condition
CREATE TABLE IF NOT EXISTS dim_weather_condition (
    condition_id SERIAL PRIMARY KEY,
    main_condition VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL
);