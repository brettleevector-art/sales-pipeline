# Sales Pipeline — a Git & GitHub lab for Data Engineers

A tiny ETL pipeline (CSV → clean → CSV + SQLite) used as a playground for learning Git and GitHub.
The code is deliberately small so you can focus on **version control**, not Python.

```
sales-pipeline/
├── data/raw/            # source CSV files (committed)
├── data/processed/      # pipeline output   (ignored by git)
├── etl/
│   ├── config.py        # settings (TAX_RATE etc.)
│   ├── extract.py       # read CSVs
│   ├── transform.py     # clean + add totals
│   └── load.py          # write CSV + SQLite
├── sql/
│   ├── create_tables.sql
│   └── reports.sql
├── tests/test_transform.py
├── pipeline.py          # entry point
└── .gitignore
```

## Run it

Requires only Python 3.8+ (no packages to install).

```bash
python pipeline.py           # run the ETL
python -m unittest -v        # run tests
```

Expected output:

```
[extract] 10 rows read
[transform] 9 rows kept, 1 dropped
[load] wrote data/processed/sales_clean.csv and table 'sales' in data/warehouse.db
```

Then follow **LAB.md**, one exercise at a time.
