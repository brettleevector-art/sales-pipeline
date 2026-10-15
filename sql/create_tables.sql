CREATE TABLE IF NOT EXISTS sales (
    order_id        INTEGER PRIMARY KEY,
    order_date      TEXT,
    customer        TEXT,
    product         TEXT,
    quantity        INTEGER,
    unit_price      REAL,
    region          TEXT,
    amount          REAL,
    amount_with_tax REAL
);
