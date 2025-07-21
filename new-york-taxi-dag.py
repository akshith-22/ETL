from airflow import DAG
import os

# GCP Operators
from airflow.providers.google.cloud.sensors import gcs
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
    ClusterGenerator,
)

# Other
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1),
}

# Environment Variables
CLUSTER_NAME = os.environ.get('CLUSTER_NAME', 'new-york-taxi-dataproc-cluster')
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', "taxi-data-project-463613")
REGION = os.environ.get('REGION', 'us-central1')
ZONE = os.environ.get('ZONE', "us-central1-a")
BUCKET_NAME = os.environ.get('BUCKET_NAME', "taxi-data-project-463613")
TRIP_DATA_FILE_NAME_PREFIX = os.environ.get('TRIP_DATA_FILE_NAME_PREFIX', "data/trip_data/trip_data_test.csv")
FARE_DATA_FILE_NAME_PREFIX = os.environ.get('FARE_DATA_FILE_NAME_PREFIX', "data/fare_data/fare_data_test.csv")
TEMP_BUCKET = os.environ.get('TEMP_BUCKET', "new-york-taxi-tutorial-project-temporary-buck")

# Cluster Configuration
CLUSTER_GENERATOR_CONFIG = ClusterGenerator(
    project_id=GCP_PROJECT_ID,
    zone=ZONE,
    master_machine_type="n1-standard-2",
    worker_machine_type="n1-standard-2",
    num_workers=0,
    worker_disk_size=300,
    master_disk_size=300,
    storage_bucket=TEMP_BUCKET,
    image_version="2.0-debian10"
).make()

# Remove invalid key (defensive step in case it's added in future)
CLUSTER_GENERATOR_CONFIG.pop("single_node_config", None)

# PySpark Job Config
PYSPARK_JOB = {
    "reference": {"project_id": GCP_PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": "gs://taxi-data-project-463613/etl_pyspark.py",
        "jar_file_uris": [
            "gs://spark-lib/bigquery/spark-3.1-bigquery-0.28.0-preview.jar"
        ]
    },
}

# DAG Definition
with DAG(
    dag_id="new-york-taxi-air",
    schedule_interval="@monthly",
    default_args=default_args,
    tags=["new-york-taxi"],
    catchup=False,
) as dag:

    check_trip_data_file = gcs.GCSObjectsWithPrefixExistenceSensor(
        task_id="check_trip_data_file",
        bucket=BUCKET_NAME,
        prefix=TRIP_DATA_FILE_NAME_PREFIX,
        google_cloud_conn_id='google_cloud_storage_default'
    )

    check_fare_data_file = gcs.GCSObjectsWithPrefixExistenceSensor(
        task_id="check_fare_data_file",
        bucket=BUCKET_NAME,
        prefix=FARE_DATA_FILE_NAME_PREFIX,
        google_cloud_conn_id='google_cloud_storage_default'
    )

    create_dataproc_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        cluster_name=CLUSTER_NAME,
        project_id=GCP_PROJECT_ID,
        region=REGION,
        cluster_config=CLUSTER_GENERATOR_CONFIG,
    )

    submit_pyspark_job = DataprocSubmitJobOperator(
        task_id="submit_pyspark_job",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=GCP_PROJECT_ID,
    )

    delete_dataproc_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster",
        project_id=GCP_PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=REGION,
    )

    [check_trip_data_file, check_fare_data_file] >> create_dataproc_cluster >> submit_pyspark_job >> delete_dataproc_cluster
