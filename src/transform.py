import pandas as pd

def _parse_timestamp(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce", dayfirst=True, infer_datetime_format=True)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Clean & normalize
    df["timestamp"] = _parse_timestamp(df["timestamp"])
    df["side"] = df["side"].astype(str).str.lower().str.strip()
    df["symbol"] = df["symbol"].astype(str).str.strip()
    df["client_type"] = df["client_type"].astype(str).str.strip()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop invalid
    df = df.dropna(subset=["timestamp","user_id","client_type","symbol","side","quantity","price"])
    df = df[df["symbol"]!=""]
    df = df[df["side"].isin(["buy","sell"])]

    # Week start (Monday)
    df["week_start_date"] = df["timestamp"].dt.to_period("W-MON").apply(lambda r: r.start_time)

    # Metrics
    df["total_volume"] = df["quantity"] * df["price"]
    sign = df["side"].map({"sell":1,"buy":-1}).fillna(0)
    df["total_pnl"] = df["quantity"] * df["price"] * sign

    # Aggregate
    agg = (df.groupby(["week_start_date","client_type","user_id","symbol"], as_index=False)
             .agg(total_volume=("total_volume","sum"),
                  total_pnl=("total_pnl","sum"),
                  trade_count=("timestamp","count")))
    return agg
