# Requirement Analysis

## Problem Statement
An e-commerce business ingests daily sales data from three disparate source systems (Customers DB, Orders System, Product Catalog) as raw CSV files stored in S3/DBFS. The goal is to design and implement an automated, reliable Databricks Medallion Architecture Data Pipeline (Bronze → Silver → Gold) and BI Dashboard that:
1. Ingests raw data seamlessly preserving historical data line-age (Bronze).
2. Cleans, validates, and flags data quality issues without dropping bad data (Silver).
3. Produces business-ready aggregations for executive analytics (Gold).
4. Serves interactive BI visualization queries for stakeholders (Dashboard).

---

## Functional Requirements

### 1. Sample Data & Anomaly Generation
- Generate 10,000 customers (`customers.csv`), 100,000 orders (`orders.csv`), and 500 products (`products.csv`).
- Inject exactly ~700 intentional quality issues (~0.7% anomaly rate):
  - `customers.csv`: 50 NULL emails (completeness), 10 duplicate `customer_id`s (uniqueness).
  - `orders.csv`: 100 NULL `customer_id`s, 200 NULL `product_id`s, 50 orphan `customer_id`s, 30 orphan `product_id`s, 20 duplicate `order_id`s.

### 2. Bronze Layer (Raw Ingestion)
- Ingest raw CSV files into Databricks Delta tables (`bronze_customers`, `bronze_orders`, `bronze_products`).
- Apply explicit schema definitions and capture audit metadata (`_ingested_at`, `_source_file`).

### 3. Silver Layer (Data Quality & Cleaning)
- Perform 4 mandatory quality checks:
  1. Completeness (No NULLs in mandatory fields).
  2. Uniqueness (No duplicate primary keys).
  3. Referential Integrity (Foreign keys exist in dimension tables).
  4. Business Rule & Range Validation (Valid dates, non-negative prices/quantities).
- Non-destructive flagging: Append `quality_check_result` (JSON struct) and `is_valid` boolean flag.
- Output a Data Quality Summary Report detailing pass rates for each table and rule.

### 4. Gold Layer (Business Aggregations)
- Filter Silver tables where `is_valid = True`.
- Build 4 materialized Gold tables:
  1. `gold_sales_by_product`: Total orders, revenue, avg order value per product.
  2. `gold_revenue_by_customer`: Total orders, revenue, lifetime value per customer.
  3. `gold_daily_weekly_trends`: Daily and weekly revenue trends and order counts.
  4. `gold_customer_segmentation`: Segment customers into High-Value, Repeat, One-Time, and Inactive cohorts.

### 5. BI Dashboard
- Provide 4 SQL visualization queries for Databricks Lakehouse Dashboards (Top Products Bar Chart, Revenue Distribution Histogram, Segmentation Pie Chart, Revenue Trend Line Chart).

---

## Non-Functional Requirements
- **Performance:** Idempotent, batch-optimised PySpark reads and writes with Delta Lake ACID transactions.
- **Maintainability:** Modular, clean code architecture separated by layers and tested via PyTest.
- **Portability:** Executable both locally in standalone PySpark and inside Databricks Repos / Workflows.

---

## Assumptions
- Raw CSV files arrive daily in S3/DBFS landing directories.
- Ingestion assumes UTF-8 encoding and comma-delimited headers.
- Customer signup dates span between 2020 and 2026.

---

## Edge Cases Handled
- **Orphan Foreign Keys:** Orders referencing non-existent customers or products are flagged as invalid in Silver and excluded from Gold aggregations.
- **Duplicate Primary Keys:** Only the first occurrence based on ingestion order is marked as valid; subsequent duplicates are flagged.
- **NULL Values in Essential Fields:** Flagged immediately in Silver checks.

---

## Clarifications & Resolution
- *Q: Should bad records be hard-deleted in Silver?*  
  *A:* No. Bad records are preserved in Silver with `is_valid = False` and detailed JSON failure reasons in `quality_check_result` for full auditing and remediation.
