import csv
import glob
import os
from etl.config import RAW_DIR


def extract():
    """Read every CSV in data/raw and return a list of row dicts."""
    rows = []
    for path in sorted(glob.glob(os.path.join(RAW_DIR, "*.csv"))):
        with open(path, newline="") as f:
            rows.extend(csv.DictReader(f))
    print(f"[extract] {len(rows)} rows read")
    return rows
