import pandas as pd
from pathlib import Path

REQUIRED_COLS = ["timestamp","user_id","client_type","symbol","side","quantity","price"]

def extract(csv_path: str) -> pd.DataFrame:
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(p)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df
