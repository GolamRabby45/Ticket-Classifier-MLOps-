# src/etl/airflow_home/dags/tickets_etl_dag.py

from datetime import datetime, timedelta
import os
import pandas as pd
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator

# In-container root; we mount your host’s ./data to /opt/airflow/data
ROOT_DIR = os.path.abspath(os.getcwd())
RAW_PATH = os.path.join(ROOT_DIR, "data", "raw", "tickets.csv")
PROCESSED_PATH = os.path.join(ROOT_DIR, "data", "processed", "tickets_processed.csv")

default_args = {
    "owner": "you",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 20),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="tickets_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    def extract():
        """
        Read the raw CSV into a temporary file.
        """
        df = pd.read_csv(RAW_PATH)
        df.to_csv("/tmp/tickets_raw.csv", index=False)

    def transform():
        """
        - Drop any rows missing the key columns in the Kaggle dataset.
        - Rename them to 'text' and 'category'.
        - Encode the category as numeric.
        """
        df = pd.read_csv("/tmp/tickets_raw.csv")
        df = df.dropna(subset=["Ticket Description", "Ticket Subject"])
        df = df.rename(columns={
            "Ticket Description": "text",
            "Ticket Subject":     "category"
        })
        df["category_code"] = df["category"].astype("category").cat.codes
        df.to_csv("/tmp/tickets_transformed.csv", index=False)

    def load():
        """
        Write out the cleaned file, and version it with DVC.
        """
        os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
        df = pd.read_csv("/tmp/tickets_transformed.csv")
        df.to_csv(PROCESSED_PATH, index=False)
        # Version with DVC
        subprocess.run(["dvc", "add", PROCESSED_PATH], check=True)

    t1 = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    t2 = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )
    t3 = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    t1 >> t2 >> t3
