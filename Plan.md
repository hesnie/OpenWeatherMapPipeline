# Plan for Apache Airflow OpenWeatherMapPipeline

## 1. API Data Extraction
- Create a DAG in `dags/weather_dag.py`.
- Create an operator or Python function to extract weather data from OpenWeatherMap API.
- Implement exception handling for API extraction.

## 2. Data Transformation using dbt
- Set up a `dbt` project in `dbt/`.
- Add a sample transformation model.
- Add a task in Airflow DAG to trigger dbt transformation.

## 3. Pipeline Orchestration
- Orchestrate extraction, transformation, and loading in the Airflow DAG.

## 4. Exception Handling in API Data Extraction
- Use try/except in API extraction task, log and raise errors.

## 5. Unit-Tests with dbt
- Add a sample dbt test in `dbt/tests/`.
- Configure the dbt model for testing.

---

## File Structure

- dags/
  - weather_dag.py
  - extract_weather.py
- dbt/
  - dbt_project.yml
  - models/
    - weather_data.sql
  - tests/
    - test_weather_data.sql
- requirements.txt