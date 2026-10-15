import unittest
from etl.transform import transform

SAMPLE = [
    {"order_id": "1", "order_date": "2026-01-01", "customer": " asha ", "product": "Mouse",
     "quantity": "2", "unit_price": "100", "region": "South"},
    {"order_id": "2", "order_date": "2026-01-01", "customer": "Rahul", "product": "Mouse",
     "quantity": "", "unit_price": "100", "region": "North"},
]


class TestTransform(unittest.TestCase):
    def test_drops_missing_quantity(self):
        self.assertEqual(len(transform(SAMPLE)), 1)

    def test_amount(self):
        self.assertEqual(transform(SAMPLE)[0]["amount"], 200)

    def test_customer_cleaned(self):
        self.assertEqual(transform(SAMPLE)[0]["customer"], "Asha")


if __name__ == "__main__":
    unittest.main()
