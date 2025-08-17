import argparse
from pathlib import Path
import pandas as pd
import plotly.express as px
from src.extract import extract
from src.transform import transform
from src.load import load_sqlite
from src.eda import run_eda

ROOT = Path(__file__).parent
CSV = ROOT / "data" / "trades.csv"
DB = ROOT / "agg_result.db"
OUTPUT = ROOT / "output"
PLOTS = OUTPUT / "plots"
DOCS = ROOT / "docs"

def main():
    parser = argparse.ArgumentParser(description="Run EDA and ETL")
    parser.add_argument("--run-eda", action="store_true", help="Run Plotly EDA and publish to docs/")
    args = parser.parse_args()

    if args.run_eda:
        run_eda(str(CSV), str(OUTPUT), str(DOCS))

    df = extract(str(CSV))
    agg = transform(df)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)

    # Save aggregated CSV and DB
    agg.to_csv(OUTPUT / "agg_trades_weekly.csv", index=False)
    load_sqlite(agg, str(DB))

    # Top-3 bronze clients (by total_volume)
    bronze = agg[agg["client_type"].str.lower()=="bronze"]
    top3 = (bronze.groupby("user_id", as_index=False)
                  .agg(total_volume=("total_volume","sum"),
                       total_pnl=("total_pnl","sum"),
                       trade_count=("trade_count","sum"))
                  .sort_values("total_volume", ascending=False)
                  .head(3))
    top3.to_csv(OUTPUT/"top_clients.csv", index=False)
    try:
        import openpyxl  # noqa
        top3.to_excel(OUTPUT/"top_clients.xlsx", index=False)
    except Exception as e:
        print("Excel export skipped (install openpyxl):", e)

    # Charts (Plotly)
    weekly = (agg.groupby(["week_start_date","client_type"], as_index=False)
                 .agg(total_volume=("total_volume","sum")))
    fig1 = px.line(weekly, x="week_start_date", y="total_volume", color="client_type",
                   markers=True, title="Weekly Total Volume by Client Type")
    fig1.write_html(str(PLOTS / "weekly_volume.html"))

    top_bronze = top3.copy()
    top_bronze["user_id"] = top_bronze["user_id"].astype(str)
    fig2 = px.bar(top_bronze, x="total_volume", y="user_id", orientation="h",
                  title="Top-3 Bronze Clients by Total Volume",
                  labels={"user_id":"user_id","total_volume":"Total Volume"})
    fig2.update_layout(yaxis={"categoryorder":"total descending"})
    fig2.write_html(str(PLOTS / "top_bronze_clients.html"))

    print("Done: outputs in ./output, DB at agg_result.db, EDA in ./docs")

if __name__ == "__main__":
    main()
