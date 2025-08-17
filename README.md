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
