import os
import csv
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def test_customers_csv_anomalies():
    filepath = os.path.join(DATA_DIR, "customers.csv")
    assert os.path.exists(filepath), "customers.csv must exist"
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        
    total_rows = len(reader)
    assert total_rows == 10010, f"Expected 10010 rows (10k + 10 dups), got {total_rows}"
    
    null_emails = sum(1 for r in reader if r["email"].strip() == "")
    assert null_emails == 50, f"Expected exactly 50 NULL emails, got {null_emails}"
    
    cids = [r["customer_id"] for r in reader]
    unique_cids = set(cids)
    assert len(cids) - len(unique_cids) == 10, "Expected 10 duplicate customer_ids"

def test_orders_csv_anomalies():
    filepath = os.path.join(DATA_DIR, "orders.csv")
    assert os.path.exists(filepath), "orders.csv must exist"
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        
    total_rows = len(reader)
    assert total_rows == 100020, f"Expected 100020 rows (100k + 20 dups), got {total_rows}"
    
    null_cids = sum(1 for r in reader if r["customer_id"].strip() == "")
    null_pids = sum(1 for r in reader if r["product_id"].strip() == "")
    assert null_cids == 100, f"Expected 100 NULL customer_ids, got {null_cids}"
    assert null_pids == 200, f"Expected 200 NULL product_ids, got {null_pids}"
