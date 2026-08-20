# Data Generation & Quality Issue Injection Notes

## Overview
`generate_sample_data.py` programmatically creates realistic e-commerce datasets with reproducible random seeding (`random.seed(42)`). It generates raw CSV files representing customers, products, and orders while intentionally injecting ~460-700 quality anomalies for testing the Silver layer validation engine.

---

## Generated File Specifications

### 1. `customers.csv`
- **Base Rows:** 10,000 unique records.
- **Total Output Rows:** 10,010 (includes 10 duplicate `customer_id` rows).
- **Intentional Anomaly Breakdown:**
  - **Completeness:** 50 rows have `email = ""` (NULL email).
  - **Uniqueness:** 10 rows duplicate an existing `customer_id` and customer profile.

### 2. `products.csv`
- **Base Rows:** 500 unique product records across 7 retail categories.
- **Total Output Rows:** 500.
- **Intentional Anomaly Breakdown:** 0 issues (serves as clean parent dimension for referential validation).

### 3. `orders.csv`
- **Base Rows:** 100,000 transaction records.
- **Total Output Rows:** 100,020 (includes 20 duplicate `order_id` rows).
- **Intentional Anomaly Breakdown:**
  - **Completeness:** 100 rows have NULL `customer_id`, 200 rows have NULL `product_id`.
  - **Referential Integrity (Orphan FKs):** 50 rows assigned non-existent `customer_id`s (999001–999050); 30 rows assigned non-existent `product_id`s (888001–888030).
  - **Uniqueness:** 20 rows duplicate an existing `order_id`.

---

## Execution Verification
To regenerate datasets, run:
```bash
python3 src/data_generation/generate_sample_data.py
```
Output files will be generated in `data/customers.csv`, `data/products.csv`, and `data/orders.csv`.
