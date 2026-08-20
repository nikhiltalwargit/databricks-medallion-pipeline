#!/usr/bin/env python3
"""
Sample Data Generator for E-Commerce Medallion Data Pipeline
Generates 10,000 customers, 100,000 orders, and 500 products with ~700 intentional data quality issues.
"""

import os
import csv
import random
from datetime import datetime, timedelta

# Seed for deterministic generation
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")
os.makedirs(DATA_DIR, exist_ok=True)

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
               "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
               "Rahul", "Priya", "Amit", "Neha", "Arjun", "Ananya", "Wei", "Mei", "Carlos", "Sofia"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Sharma", "Verma", "Patel", "Singh", "Chen", "Wang", "Zhang", "Kim", "Lee", "Lopez", "Gonzalez"]

DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "company.org", "techcorp.io"]
COUNTRIES = ["United States", "India", "Germany", "United Kingdom", "Canada", "Australia", "France", "Japan", "Brazil"]
SEGMENTS = ["Basic", "Standard", "Premium"]
CATEGORIES = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports & Outdoors", "Beauty & Care", "Toys & Games"]
ORDER_STATUSES = ["Completed", "Pending", "Cancelled"]

def random_date(start_year=2020, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 8, 20)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_customers(num_rows=10000):
    print(f"Generating {num_rows} customers...")
    filepath = os.path.join(DATA_DIR, "customers.csv")
    customers = []
    
    for cid in range(1, num_rows + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{cid}@{random.choice(DOMAINS)}"
        country = random.choice(COUNTRIES)
        signup = random_date(2020, 2025)
        segment = random.choice(SEGMENTS)
        ltv = round(random.uniform(50.0, 5000.0), 2)
        customers.append({
            "customer_id": cid,
            "customer_name": name,
            "email": email,
            "country": country,
            "signup_date": signup,
            "customer_segment": segment,
            "lifetime_value": ltv
        })

    # Anomaly Injection 1: 50 NULL emails
    null_email_indices = random.sample(range(num_rows), 50)
    for idx in null_email_indices:
        customers[idx]["email"] = ""

    # Anomaly Injection 2: 10 duplicate customer_id rows
    dup_indices = random.sample(range(num_rows), 10)
    for idx in dup_indices:
        dup_row = customers[idx].copy()
        # append duplicated customer
        customers.append(dup_row)

    # Write to CSV
    fieldnames = ["customer_id", "customer_name", "email", "country", "signup_date", "customer_segment", "lifetime_value"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customers)
        
    print(f"Saved customers.csv with {len(customers)} rows (including 10 duplicates).")
    return [c["customer_id"] for c in customers if c["customer_id"] != ""]

def generate_products(num_rows=500):
    print(f"Generating {num_rows} products...")
    filepath = os.path.join(DATA_DIR, "products.csv")
    products = []
    
    for pid in range(1, num_rows + 1):
        cat = random.choice(CATEGORIES)
        pname = f"{cat} Item #{pid}"
        price = round(random.uniform(10.0, 1500.0), 2)
        cost = round(price * random.uniform(0.4, 0.8), 2)
        stock = random.randint(10, 500)
        reorder = random.randint(5, 50)
        products.append({
            "product_id": pid,
            "product_name": pname,
            "category": cat,
            "price": price,
            "cost": cost,
            "stock_quantity": stock,
            "reorder_level": reorder
        })

    fieldnames = ["product_id", "product_name", "category", "price", "cost", "stock_quantity", "reorder_level"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
        
    print(f"Saved products.csv with {len(products)} rows.")
    return [p["product_id"] for p in products]

def generate_orders(valid_cids, valid_pids, num_rows=100000):
    print(f"Generating {num_rows} orders...")
    filepath = os.path.join(DATA_DIR, "orders.csv")
    orders = []
    
    for oid in range(1, num_rows + 1):
        cid = random.choice(valid_cids)
        pid = random.choice(valid_pids)
        odate = random_date(2023, 2026)
        qty = random.randint(1, 10)
        unit_price = round(random.uniform(15.0, 500.0), 2)
        total_amt = round(qty * unit_price, 2)
        status = random.choice(ORDER_STATUSES)
        pay_date = odate if status == "Completed" else ""
        
        orders.append({
            "order_id": oid,
            "customer_id": cid,
            "order_date": odate,
            "product_id": pid,
            "quantity": qty,
            "unit_price": unit_price,
            "total_amount": total_amt,
            "order_status": status,
            "payment_date": pay_date
        })

    # Anomaly Injection 1: 100 rows with NULL customer_id
    null_cid_indices = random.sample(range(num_rows), 100)
    for idx in null_cid_indices:
        orders[idx]["customer_id"] = ""

    # Anomaly Injection 2: 200 rows with NULL product_id
    null_pid_indices = random.sample(range(num_rows), 200)
    for idx in null_pid_indices:
        orders[idx]["product_id"] = ""

    # Anomaly Injection 3: 50 orphan customer_ids (999001 - 999050)
    orphan_cid_indices = random.sample([i for i in range(num_rows) if i not in null_cid_indices], 50)
    for i, idx in enumerate(orphan_cid_indices):
        orders[idx]["customer_id"] = 999001 + i

    # Anomaly Injection 4: 30 orphan product_ids (888001 - 888030)
    orphan_pid_indices = random.sample([i for i in range(num_rows) if i not in null_pid_indices], 30)
    for i, idx in enumerate(orphan_pid_indices):
        orders[idx]["product_id"] = 888001 + i

    # Anomaly Injection 5: 20 duplicate order_id rows
    dup_oid_indices = random.sample(range(num_rows), 20)
    for idx in dup_oid_indices:
        dup_row = orders[idx].copy()
        orders.append(dup_row)

    fieldnames = ["order_id", "customer_id", "order_date", "product_id", "quantity", "unit_price", "total_amount", "order_status", "payment_date"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
        
    print(f"Saved orders.csv with {len(orders)} rows (including 20 duplicates).")

if __name__ == "__main__":
    cids = generate_customers(10000)
    pids = generate_products(500)
    generate_orders(cids, pids, 100000)
    print("All sample datasets generated successfully!")
