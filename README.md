# Trades ETL Pipeline

#### End-to-end ETL pipeline with CI/CD, interactive EDA reports, and Tableau dashboard for trade data.

## Project Goal

Implement an ETL pipeline to process client trade data from CSV, aggregate results, and store them in a database.  
Demonstrate CI/CD setup and readiness for scaling.

## Project Structure

```
trades_etl_full_repo/
├─ data/                  # CSV templates or example datasets
├─ output/                # ETL results, reports, top clients
├─ etl/
│  ├─ extract.py          # data extraction module
│  ├─ transform.py        # transformation and aggregation module
│  ├─ load.py             # load module into DB
├─ reports/
│  └─ eda_report.html     # automatic EDA report
├─ Dockerfile             # for containerizing ETL
├─ .github/workflows/
│  └─ etl_pipeline.yml    # CI/CD via GitHub Actions
├─ agg_result.db          # SQLite DB with aggregated results
├─ README.md
└─ requirements.txt       # Python dependencies
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run ETL Pipeline

Run each step of the ETL manually:

```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

Results are saved in `agg_result.db` and `output/top_clients.xlsx` (or `.csv`).

## Run EDA

Generate an interactive EDA report from a CSV file:

```bash
python etl/eda.py data/trades_sample.csv
```

- HTML report saved to `output/eda_report.html` and `docs/eda_report.html`  
- Reports contain interactive Plotly charts for data distributions, aggregations, and trade analysis  
- Public hosted report: [EDA Report](https://oleksiy-danilin.github.io/Trades_ETL/eda_report.html)

## CI/CD

- GitHub Actions automatically triggers the ETL on **push** or **workflow_dispatch**  
- Full sequence executed: `extract → transform → load`  
- Reports and top clients are created in `output/`

## Additional Components

- **EDA:** Automatic Exploratory Data Analysis checks CSV quality and detects outliers, missing values, and inappropriate formats  
- **HTML Report:** Interactive HTML report visualizes distributions and aggregations for quick data quality checks  
- **Docker:** Ensures ETL runs reliably and reproducibly, even if data volume increases sharply  
- **Tableau Dashboard:** Interactive dashboard prototype built on EDA-cleaned database.  
  Public demo version: [Trade Performance Dashboard](https://public.tableau.com/app/profile/oleksiy.danilin/viz/TradePerformanceDashboard_17548689918890/TRADEPERFORMANCEDASHBOARD)

## Data Aggregation

- Convert `timestamp` to `week_start_date` (Monday)  

**Aggregate by:**
- `week_start_date`
- `client_type` (gold, silver, bronze)
- `user_id`
- `symbol`

**Compute:**
- `total_volume`
- `trade_count`
- `total_pnl` (optional)

Save results in `agg_trades_weekly` table in `agg_result.db`.

## Reporting

- Interactive charts from aggregated data (via HTML EDA report)  
- Top 3 bronze clients selected by `total_volume` and `total_pnl`  
- Saved results in `output/top_clients.xlsx` or `.csv`

## Scalability

ETL pipeline designed to handle larger volumes in the future (>100M rows):

- **Storage:** migrate from SQLite to BigQuery (GCP) or Snowflake (AWS)  
- **Orchestration:** Airflow, Prefect, or dbt for DAG management  
- **Distributed processing:** Spark or Dask  
- **Monitoring:** track execution time, processed records, transformation errors, missing data  
- **Data storage:** raw CSVs in S3/Blob, aggregated results in SQL/NoSQL  

See `ETL_Scaling_Trades_RU.pdf` for details.
