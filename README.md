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

#### Install Dependencies
--------------------
pip install -r requirements.txt

#### Run ETL
-------
Run each step of the ETL manually:

python etl/extract.py

python etl/transform.py

python etl/load.py

Results are saved in agg_result.db and output/top_clients.xlsx (or .csv).

## Run ETL

```bash
python etl/extract.py
python etl/transform.py
python etl/load.py

#### CI/CD
-----
GitHub Actions automatically triggers the ETL on push or workflow_dispatch.

Pipeline runs full sequence: extract -> transform -> load

Reports and top clients are created in output/

#### Additional Components
---------------------
EDA: Automatic Exploratory Data Analysis checks CSV quality and detects outliers, missing values, and/or inappropriate data formats.

HTML-report: Interactive HTML report visualizes distributions and aggregations for quick data quality checks. Check it at: https://oleksiy-danilin.github.io/Trades_ETL/eda_report.html

Docker: Added for demonstrative purposes, although the data volume is small. Containerization ensures ETL can run reliably even if data volume increases sharply, guaranteeing reproducibility across environments.

Tableau Dashboard: Built on an EDA-cleaned database. Prototype an interactive dashboard instead of isolated static plots. Public demo version: https://public.tableau.com/app/profile/oleksiy.danilin/viz/TradePerformanceDashboard_17548689918890/TRADEPERFORMANCEDASHBOARD 

#### Data Aggregation
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

#### Reporting
---------
- Build charts from aggregated data (replaced by the Tableau dashboard, which features interactive filters and complex feature analysis)
- Select top-3 bronze clients by total_volume and total_pnl
- Save results: output/top_clients.xlsx or .csv

#### Scalability
-----------
ETL pipeline designed to handle larger volumes in the future (>100M rows):
- Storage: migrate from SQLite to BigQuery (GCP) or Snowflake (AWS)
- Orchestration: Airflow, Prefect, or dbt for DAG management
- Distributed processing: Spark or Dask
- Monitoring: track execution time, processed records, transformation errors, missing data
- Data storage: raw CSVs in S3/Blob, aggregated results in SQL/NoSQL
- See ETL_Scaling_Trades_RU.pdf for details
