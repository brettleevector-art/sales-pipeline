import csv
import os
import sqlite3
from etl.config import PROCESSED_DIR, DB_PATH


def load(rows):
    """Write clean rows to a CSV and a SQLite table."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out = os.path.join(PROCESSED_DIR, "sales_clean.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    with sqlite3.connect(DB_PATH) as con:
        con.executescript(open("sql/create_tables.sql").read())
        con.executemany(
            "INSERT OR REPLACE INTO sales VALUES (:order_id,:order_date,:customer,:product,"
            ":quantity,:unit_price,:region,:amount,:amount_with_tax)",
            rows,
        )
    print(f"[load] wrote {out} and table 'sales' in {DB_PATH}")
