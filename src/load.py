import sqlite3
from pathlib import Path
import pandas as pd

def load_sqlite(df: pd.DataFrame, db_path: str, table: str = "agg_trades_weekly"):
    p = Path(db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(p)
    try:
        df.to_sql(table, con, if_exists="replace", index=False)
    finally:
        con.close()
