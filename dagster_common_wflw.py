from dagster import job, op, resource, Definitions, Config

# 1. Define configuration
class MyConfig(Config):
    param1: str
    param2: int

# 2. Define resources
@resource
def my_resource(init_context):
    # Initialize and return a resource (e.g., database connection)
    return "Resource initialized"

# 3. Define ops (formerly tasks)
@op
def extract(context, config: MyConfig):
    context.log.info(f"Extracting data with {config.param1}")
    return "extracted_data"

@op
def transform(context, input_data):
    context.log.info("Transforming data")
    return "transformed_data"

@op
def load(context, input_data):
    context.log.info("Loading data")
    return "Data loaded successfully"

# 4. Define job (pipeline)
@job(resource_defs={"my_resource": my_resource})
def my_etl_job():
    load(transform(extract()))

# 5. Define Definitions for deployment
defs = Definitions(
    jobs=[my_etl_job],
    resources={
        "my_resource": my_resource
    }
)

# 6. For local testing
if __name__ == "__main__":
    result = my_etl_job.execute_in_process(
        run_config={
            "ops": {
                "extract": {
                    "config": {
                        "param1": "test",
                        "param2": 42
                    }
                }
            }
        }
    )
    print("Job result:", result.success)