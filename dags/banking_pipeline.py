from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import psycopg2

def check_db_health():
    conn = psycopg2.connect(
        dbname="banking_db", user="postgres",
        password="abhishek", host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"Total transactions in DB: {count}")
    conn.close()

def run_spark_job():
    subprocess.run(
        ["python", "C:/Users/KIIT0001/OneDrive/Documents/Data/spark_analysis.py"],
        check=True
    )

default_args = {
    'owner': 'abhishek',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='banking_pipeline',
    default_args=default_args,
    description='Core Banking Data Pipeline',
    schedule='@daily',
    start_date=datetime(2026, 4, 18),
    catchup=False
) as dag:

    health_check = PythonOperator(
        task_id='check_db_health',
        python_callable=check_db_health
    )

    spark_job = PythonOperator(
        task_id='run_spark_analytics',
        python_callable=run_spark_job
    )

    health_check >> spark_job