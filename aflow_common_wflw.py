from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my_workflow',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define Python functions for tasks
def task_1():
    print("Executing Task 1")

def task_2():
    print("Executing Task 2")

# Define tasks
task_1 = PythonOperator(
    task_id='task_1',
    python_callable=task_1,
    dag=dag,
)

task_2 = PythonOperator(
    task_id='task_2',
    python_callable=task_2,
    dag=dag,
)

task_3 = BashOperator(
    task_id='task_3',
    bash_command='echo "Executing Task 3"',
    dag=dag,
)

# Set task dependencies
task_1 >> task_2 >> task_3