

```
services:
  airflow-scheduler:
    image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.3}
    environment:
      - AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL=0
      - AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=60
    # ... other configuration options
```