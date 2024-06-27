from dagster import job, op, repository

@op
def hello():
    return "Hello, Dagster!"

@job
def my_job():
    hello()

@repository
def my_repository():
    return [my_job]
