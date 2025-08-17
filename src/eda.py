from pathlib import Path
import pandas as pd
import plotly.express as px

def run_eda(csv_path: str, output_dir: str = "output", docs_dir: str = "docs"):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    docs = Path(docs_dir); docs.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    # Parse types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True, infer_datetime_format=True)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["side"] = df["side"].astype(str).str.lower().str.strip()

    # Basic stats
    stats = {
        "rows": len(df),
        "rows_valid_ts": int(df["timestamp"].notna().sum()),
        "nulls_per_column": df.isna().sum().to_dict(),
        "unique_symbols": int(df["symbol"].nunique() if "symbol" in df.columns else 0),
        "date_min": str(df["timestamp"].min()),
        "date_max": str(df["timestamp"].max()),
    }
    (out/"eda_report.csv").write_text(pd.Series(stats, dtype="object").to_csv())

    # Clean subset for charts
    d = df.dropna(subset=["timestamp","symbol","quantity","price"]).copy()
    d["total_value"] = d["quantity"] * d["price"]
    d["week_start_date"] = d["timestamp"].dt.to_period("W-MON").apply(lambda r: r.start_time)

    figs = []

    if "client_type" in d.columns:
        figs.append(px.histogram(d, x="client_type", title="Trades by Client Type"))

    if "symbol" in d.columns:
        vol = d.groupby("symbol", as_index=False)["total_value"].sum().sort_values("total_value", ascending=False)
        figs.append(px.bar(vol, x="symbol", y="total_value", title="Total Traded Value by Symbol"))

    weekly = d.groupby(["week_start_date","client_type"], as_index=False)["total_value"].sum()
    if not weekly.empty and "client_type" in weekly.columns:
        figs.append(px.line(weekly, x="week_start_date", y="total_value", color="client_type", markers=True,
                            title="Weekly Total Value by Client Type"))

    # Buy vs Sell counts
    if "side" in d.columns:
        side_cnt = d.groupby("side", as_index=False)["total_value"].sum()
        figs.append(px.bar(side_cnt, x="side", y="total_value", title="Buy vs Sell — Total Value"))

    # Compose HTML and save to output/ and docs/
    html = ["<html><head><meta charset='utf-8'><title>EDA Report</title></head><body>",
            "<h1>EDA Report</h1>",
            f"<p><b>Rows:</b> {stats['rows']} | <b>Valid timestamps:</b> {stats['rows_valid_ts']}</p>",
            "<h2>Charts</h2>"]
    for i, fig in enumerate(figs, 1):
        html.append(f"<h3>Figure {i}</h3>")
        html.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    html.append("</body></html>")
    html = "\n".join(html)

    for target in [(out/"eda_report.html"), (docs/"eda_report.html")]:
        target.write_text(html, encoding="utf-8")

    # Index for Pages
    (docs/"index.html").write_text("<html><head><meta charset='utf-8'><title>Reports</title></head>"
                                   "<body><h1>Reports</h1><ul>"
                                   "<li><a href='eda_report.html'>EDA Report</a></li>"
                                   "</ul></body></html>", encoding="utf-8")

    print("EDA ready at output/eda_report.html and docs/eda_report.html")
