## Trades ETL Pipeline

### English Version

#### Project Goal
Implement an ETL pipeline to process client trade data from CSV, aggregate results, and store them in a database. Demonstrate CI/CD setup and readiness for scaling.

#### Project Structure
```
trades_etl_full_repo/
├─ data/ # CSV templates or example datasets
├─ output/ # ETL results, reports, top clients
├─ etl/
│ ├─ extract.py # data extraction module
│ ├─ transform.py # transformation and aggregation module
│ ├─ load.py # load module into DB
├─ reports/
│ └─ eda_report.html # automatic EDA report
├─ Dockerfile # for containerizing ETL
├─ .github/workflows/
│ └─ etl_pipeline.yml # CI/CD via GitHub Actions
├─ agg_result.db # SQLite DB with aggregated results
├─ README.md
└─ requirements.txt # Python dependencies
```

####INSTALL DEPENDENCIES
--------------------
pip install -r requirements.txt

RUN ETL
-------
python etl/extract.py
python etl/transform.py
python etl/load.py
Results are saved in agg_result.db and output/top_clients.xlsx (or .csv).

CI/CD
-----
GitHub Actions automatically triggers the ETL on push or workflow_dispatch.
Pipeline runs full sequence: extract -> transform -> load
Reports and top clients are created in output/

ADDITIONAL COMPONENTS
---------------------
EDA: Automatic Exploratory Data Analysis checks CSV quality and detects outliers or missing values.

HTML-report: Interactive HTML report visualizes distributions and aggregations for quick data quality checks.

Docker: Containerization ensures ETL can run reliably even if data volume increases sharply, guaranteeing reproducibility across environments.

Tableau Dashboard: Built on cleaned data after EDA. Prototype interactive dashboard instead of static plots.

DATA AGGREGATION
----------------
- Convert timestamp to week_start_date (Monday)
- Aggregate by:
  * week_start_date
  * client_type (gold, silver, bronze)
  * user_id
  * symbol
- Compute:
  * total_volume
  * trade_count
  * total_pnl (optional)
- Save results in agg_trades_weekly table in agg_result.db

REPORTING
---------
- Build charts from aggregated data (optional)
- Select top-3 bronze clients by total_volume and total_pnl
- Save results: output/top_clients.xlsx or .csv

SCALABILITY
-----------
ETL pipeline designed to handle larger volumes in the future (>100M rows):
- Storage: migrate from SQLite to PostgreSQL / BigQuery / Snowflake
- Orchestration: Airflow, Prefect, or dbt for DAG management
- Distributed processing: Spark or Dask
- Monitoring: track execution time, processed records, transformation errors, missing data
- Data storage: raw CSVs in S3/Blob, aggregated results in SQL/NoSQL
See Scalability_Overview.pdf for details
