#FROM astrocrpublic.azurecr.io/runtime:2.7.0

#RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
#    pip install --no-cache-dir dbt-sqlserver && deactivate


FROM quay.io/astronomer/astro-runtime:8.8.0

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-sqlserver && deactivate

ENV AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES = airflow\.* astro\.*