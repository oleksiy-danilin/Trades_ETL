## Trades ETL Pipeline

### English Version

#### Project Goal
Implement an ETL pipeline to process client trade data from CSV, aggregate results, and store them in a database. Demonstrate CI/CD setup and readiness for scaling.

### Project Structure
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

### Running ETL Manually
Install dependencies:
```bash
pip install -r requirements.txt
Run ETL:
python etl/extract.py
python etl/transform.py
python etl/load.py
Results are saved in agg_result.db and output/top_clients.xlsx (or .csv).
CI/CD
GitHub Actions automatically triggers the ETL on push or workflow_dispatch.
The pipeline runs the full sequence: extract → transform → load.
After execution, reports and top clients are created in output/.
Additional Components: EDA, HTML-report, Docker, Tableau Dashboard
EDA: Automatic Exploratory Data Analysis checks CSV quality and detects outliers or missing values.
HTML-report: Interactive HTML report visualizes distributions and aggregations for quick data quality checks.
Docker: Containerization ensures ETL can run reliably even if data volume increases sharply, guaranteeing reproducibility across environments.
Tableau Dashboard: Built on cleaned data after EDA. This interactive dashboard serves as a prototype for more modern “live” dashboard solutions instead of static plots.
Data Aggregation
Convert timestamp to week_start_date (Monday).
Aggregate by:
week_start_date
client_type (gold, silver, bronze)
user_id
symbol
Compute:
total_volume
trade_count
total_pnl (optional)
Save results in agg_trades_weekly table in agg_result.db.
Reporting
Build charts from aggregated data (optional).
Select top-3 bronze clients by total_volume and total_pnl.
Save results: output/top_clients.xlsx or .csv.
Scalability
The ETL pipeline is designed to handle larger volumes in the future. For datasets >100M rows:
Storage: migrate from SQLite to PostgreSQL / BigQuery / Snowflake.
ETL orchestration: use Airflow, Prefect, or dbt for DAG management.
Distributed processing: leverage Spark or Dask.
Monitoring: track ETL metrics: execution time, processed records, transformation errors, missing data.
Data storage: raw CSVs in S3/Blob, aggregated results in SQL/NoSQL databases.
A separate PDF (Scalability_Overview.pdf) provides detailed explanations of these cloud-based scaling options.
Русская версия
Цель проекта
Реализовать ETL-пайплайн для обработки торговых данных клиентов из CSV, агрегировать результаты и сохранять их в базу данных. Продемонстрировать настройку CI/CD и готовность решения к масштабированию.
Структура проекта
trades_etl_full_repo/
├─ data/                  # исходные CSV-шаблоны или примеры данных
├─ output/                # результаты ETL, отчеты, топ-клиенты
├─ etl/
│  ├─ extract.py          # модуль извлечения данных
│  ├─ transform.py        # модуль трансформации и агрегации
│  ├─ load.py             # модуль загрузки в БД
├─ reports/
│  └─ eda_report.html     # автоматический EDA-отчет
├─ Dockerfile             # для контейнеризации ETL
├─ .github/workflows/
│  └─ etl_pipeline.yml    # CI/CD через GitHub Actions
├─ agg_result.db           # база данных SQLite с агрегированными данными
├─ README.md
└─ requirements.txt       # зависимости Python
Запуск ETL вручную
Установите зависимости:
pip install -r requirements.txt
Запустите ETL:
python etl/extract.py
python etl/transform.py
python etl/load.py
Результаты сохраняются в agg_result.db и output/top_clients.xlsx (или .csv).
CI/CD
GitHub Actions автоматически запускает ETL при push или workflow_dispatch.
Пайплайн выполняет последовательность: extract → transform → load.
После выполнения создаются отчеты и топ-клиенты в output/.
Дополнительно: EDA, HTML-отчет, Docker, Tableau Dashboard
EDA: Автоматический анализ данных проверяет качество CSV, выявляет выбросы и пропуски.
HTML-отчет: Интерактивный HTML-отчет позволяет быстро визуализировать распределения и агрегации, удобно для контроля качества данных.
Docker: Контейнеризация обеспечивает работу ETL даже при резком увеличении объема данных, гарантируя воспроизводимость в любом окружении.
Tableau Dashboard: Создан на очищенных данных после EDA. Этот интерактивный дэшборд служит прототипом более современного решения «живых» дэшбордов вместо статичных графиков.
Агрегация данных
Преобразование timestamp в week_start_date (понедельник).
Агрегация по:
week_start_date
client_type (gold, silver, bronze)
user_id
symbol
Рассчитываем:
total_volume
trade_count
total_pnl (опционально)
Результат сохраняется в таблицу agg_trades_weekly в базе agg_result.db.
Отчётность
Построение графиков по агрегированным данным (по желанию).
Выбор топ-3 бронзовых клиентов по total_volume и total_pnl.
Сохранение результатов: output/top_clients.xlsx или .csv.
Масштабирование
ETL-пайплайн разработан для обработки больших объемов данных в будущем. Для наборов данных >100 млн строк рекомендуется:
Хранилище: переход с SQLite на PostgreSQL, BigQuery или Snowflake.
Оркестрация ETL: использование Airflow, Prefect или dbt для управления DAG.
Распределённая обработка: Spark или Dask.
Мониторинг: отслеживание метрик ETL: время выполнения, количество обработанных записей, ошибки трансформации, пропуски.
Хранение данных: входные CSV в S3/Blob, агрегированные результаты в SQL/NoSQL.
Отдельный PDF (Scalability_Overview.pdf) содержит подробное описание этих решений и архитектурных подходов для масштабирования ETL в облаке.

Старая версия!!!!

# Trades ETL + Plotly EDA (готовый репозиторий)

**Что внутри**
- `data/trades.csv` — демо-датасет (замените на свой, сохранив те же заголовки).
- `src/` — модули ETL (`extract.py`, `transform.py`, `load.py`) и `eda.py`.
- `main.py` — один вход: запускает EDA (опция) и весь ETL.
- `output/` — агрегаты, графики и Top-3 bronze клиентов (`csv` и `xlsx`).
- `docs/eda_report.html` — интерактивный EDA‑отчёт (готов для GitHub Pages).
- Dockerfile, GitHub Actions workflow, requirements.txt.

## Запуск (локально, macOS)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py --run-eda
# Откройте: docs/eda_report.html
```

## Замените датасет
Подставьте ваш CSV как `data/trades.csv` **с теми же колонками**:
`timestamp,user_id,client_type,symbol,side,quantity,price` (поддержан формат даты `DD/MM/YYYY HH:MM`).

## Docker
```bash
docker build -t trades-etl .
docker run --rm -v "$(pwd)/output:/app/output" -v "$(pwd)/docs:/app/docs" trades-etl
```

## CI/CD (GitHub Actions)
- Workflow: `.github/workflows/etl.yml`
- Триггеры: push и ручной `workflow_dispatch`
- Артефакты: `agg_result.db`, `output/`, `docs/`

## Публикация EDA на GitHub Pages
1. Убедитесь, что `docs/eda_report.html` создан (`python main.py --run-eda`).
2. Settings → Pages: **Deploy from a branch**, **Branch**: `main` + `/docs`.
3. Откройте: `https://<логин>.github.io/<repo>/eda_report.html`

## Почему EDA и Docker
- **EDA**: контроль качества данных, прозрачность, ускорение адаптации под изменения CSV.
- **Docker**: одинаковое окружение, готовность к масштабированию, лёгкий деплой.

## Масштабирование (100M+ строк)
- Хранение: Parquet (S3/GCS), каталогизация (AWS Glue/BigQuery).
- Обработка: Spark/Dask/BigQuery SQL, партиционирование по неделям.
- DWH: Redshift/Snowflake/BigQuery.
- Оркестрация/мониторинг: Airflow/Prefect, Prometheus/Grafana, алерты.
