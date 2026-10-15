from etl.config import TAX_RATE


def transform(rows):
    """Drop rows with missing quantity, cast types, add totals."""
    clean = []
    for r in rows:
        if not r["quantity"]:
            continue
        qty = int(r["quantity"])
        price = float(r["unit_price"])
        amount = qty * price
        clean.append({
            "order_id": int(r["order_id"]),
            "order_date": r["order_date"],
            "customer": r["customer"].strip().title(),
            "product": r["product"],
            "quantity": qty,
            "unit_price": price,
            "region": r["region"],
            "amount": round(amount, 2),
            "amount_with_tax": round(amount * (1 + TAX_RATE), 2),
        })
    print(f"[transform] {len(clean)} rows kept, {len(rows) - len(clean)} dropped")
    return clean
