from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import logging

# 1. Configure logging
logging.basicConfig(level=logging.INFO)

# 2. Define tasks
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract(param: str):
    logging.info(f"Extracting data with param: {param}")
    return f"extracted_data_{param}"

@task
def transform(data: str):
    logging.info(f"Transforming data: {data}")
    return f"transformed_{data}"

@task
def load(data: str):
    logging.info(f"Loading data: {data}")
    return f"loaded_{data}"

# 3. Define main flow
@flow(name="ETL Flow", description="A simple ETL workflow")
def etl_flow(param: str = "default"):
    extracted_data = extract(param)
    transformed_data = transform(extracted_data)
    result = load(transformed_data)
    return result

# 4. Run the flow
if __name__ == "__main__":
    result = etl_flow("test_param")
    print(f"Flow result: {result}")