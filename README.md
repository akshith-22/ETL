# Building-ETL-Pipeline-in-Google-Cloud-Platform-A-Project-Based-Guide-with-PySpark-and-Airflow

The project flow is as below
![d859bbaa-fcff-4b2d-8362-2955bdc5ebe7](https://github.com/user-attachments/assets/340a48ad-bde8-40b4-8f67-321a069c5beb)

Key Responsibilities & Technologies:

    Data Ingestion & Storage: Automated ingestion of raw data (e.g., CSV/JSON) into Cloud Storage.

    Big‑Data Processing: Developed PySpark scripts running on Dataproc to perform batch transformations and aggregations.

    Workflow Orchestration: Built Airflow DAGs (via Cloud Composer) to manage end-to-end process, including:

        Uploading scripts to GCS

        Dynamic branching (weekday vs. weekend logic) to trigger distinct PySpark tasks
        github.com

        Creation and deletion of Dataproc clusters to optimize resource use

    Data Loading & Analytics: Processed data loaded into BigQuery for querying, and outputs persisted in GCS for downstream consumption.

    Automation & Scalability: Configured scheduled daily runs with full retry and failure handling; dynamically scaled compute infrastructure.

Outcomes & Impact:

    Achieved fully automated, scalable ETL process closely resembling enterprise-grade data pipelines.

    Demonstrated cost-efficiency by spinning clusters on‑demand and tearing them down post‑processing.

    Gained hands‑on expertise with GCP services (Composer, Dataproc, GCS, BigQuery), PySpark, and Airflow—key skills for modern data engineering roles.

