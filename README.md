# OpenWeatherMapPipeline

This project provides an end-to-end data pipeline for ingesting, transforming, and modeling weather data from the Meteomatics/OpenWeatherMap API. The pipeline is orchestrated with Apache Airflow, stores raw and processed data in Azure SQL, and uses dbt for data modeling into a star schema suitable for analytics.

---

## Project Structure

```
dags/
  weather_dag.py                # Airflow DAG for orchestrating the pipeline
  dbt/
    open_weather_map/
      dbt_project.yml           # dbt project configuration
      profile.yml               # dbt profile for Azure SQL connection
      sources.yml               # dbt sources definition
      packages.yml              # dbt packages (includes dbt_date)
      seeds/
        weather_code_information.csv  # Weather code lookup (seed data)
      models/
        staging/
          stg_weather.sql           # Staging model for raw weather data
          stg_locations.sql         # Staging model for station/location data
          stg_weather_condition.sql # Staging model for weather codes
        mart/
          dim_date.sql              # Date dimension (uses dbt_date)
          dim_locations.sql         # Location dimension
          dim_weather_condition.sql # Weather condition dimension
          fact_weather.sql          # Fact table for weather observations
          generic_tests.yml         # Generic dbt tests for data quality
      tests/
        test_weather_data.sql       # Custom test for weather data
```

---

## Pipeline Overview

1. **Data Ingestion**  
   - The Airflow DAG (`weather_dag.py`) fetches weather and station data from the Meteomatics API.
   - Raw data is saved to Azure Blob Storage and Azure SQL Database.

2. **Data Modeling with dbt**  
   - Raw data is staged using dbt models in the `staging/` folder.
   - Weather codes are loaded from the CSV seed (`weather_code_information.csv`).
   - Star schema is built in the `mart/` folder with dimension and fact tables.

3. **Testing & Quality**  
   - dbt generic and custom tests ensure data quality (e.g., not null, unique, valid temperature ranges).

---

## Setup & Usage

### Prerequisites

- Docker (for Airflow and dependencies)
- Azure SQL Database (or compatible SQL Server)
- Python 3.8+
- dbt (with SQL Server adapter)
- Access to Meteomatics API

### 1. Clone the Repository

```sh
git clone https://github.com/hesnie/OpenWeatherMapPipeline.git
cd OpenWeatherMapPipeline
```

### 2. Configure Environment

- Set up environment variables for Azure SQL and API credentials (see `weather_dag.py` and `profile.yml`).
- Adjust connection details in `profile.yml` as needed.

### 3. Start Airflow (Docker)

```sh
docker-compose up -d
```

### 4. Initialize dbt

```sh
cd dags/dbt/open_weather_map
dbt deps         # Install dbt packages
dbt seed         # Load seed data (weather codes)
dbt run          # Build models
dbt test         # Run data tests
```

### 5. Run the Pipeline

- Trigger the Airflow DAG via the Airflow UI or CLI.

---

## Data Model

- **Dimensions:**
  - `dim_date`: Calendar dates (generated with dbt_date)
  - `dim_locations`: Weather station metadata
  - `dim_weather_condition`: Weather code descriptions (from CSV seed)
- **Fact Table:**
  - `fact_weather`: Hourly weather observations, linked to all dimensions

---

## Testing

- Generic dbt tests are defined in `mart/generic_tests.yml`.
- Custom SQL tests are in `tests/`.

---

## References

- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Airflow](https://airflow.apache.org/)
- [Meteomatics API](https://www.meteomatics.com/en/api/)
- [Meteomatics Python Data Connector](https://github.com/meteomatics/python-connector-api/tree/master/examples/notebooks)
- [Azure SQL Database](https://azure.microsoft.com/en-us/products/azure-sql/database/)

---

## Maintainer

Henrik S Nielsen
