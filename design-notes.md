# Design Notes — Medallion Architecture Pipeline

## Architecture Overview

```
[ Landing CSVs ] (S3 / DBFS / local data/)
       │
       ▼
 [ Bronze Layer ]  ── Raw Ingestion into Delta Tables + Ingestion Metadata
       │           (bronze_customers, bronze_orders, bronze_products)
       ▼
 [ Silver Layer ]  ── Data Quality Validation & Non-Destructive Flagging
       │           (silver_customers, silver_orders, silver_products)
       │           └── Appends `is_valid` & `quality_check_result`
       ▼
  [ Gold Layer ]   ── Business Aggregations (Only `is_valid = True` records)
       │           (gold_sales_by_product, gold_revenue_by_customer,
       │            gold_daily_weekly_trends, gold_customer_segmentation)
       ▼
 [ BI Dashboard ]  ── Databricks SQL Queries & Visualizations
```

---

## Data Layer Design

### 1. Bronze Layer (Raw Ingestion)
- **Goal:** Ingest raw CSV data without altering business content.
- **Implementation:** PySpark DataFrame API reading CSV with explicit schemas.
- **Metadata Enriched:**
  - `_ingested_at`: Current timestamp at ingestion time.
  - `_source_file`: File path of the raw CSV file.

### 2. Silver Layer (Cleaned & Tagged Data)
- **Goal:** Enforce data quality non-destructively.
- **Validation Engine:** Modular PySpark functions evaluating 4 quality dimensions:
  1. `completeness`: Null checks on mandatory columns.
  2. `uniqueness`: Window-based row numbering over primary keys.
  3. `type_validation`: Range checks (`quantity > 0`, `unit_price >= 0`).
  4. `referential_integrity`: Left anti-joins against dimension tables.
- **Output Column Structure:**
  - `is_valid`: Boolean flag (`True` if passed all checks, `False` otherwise).
  - `quality_check_result`: String/JSON listing check names and failure reasons.

### 3. Gold Layer (Curated Aggregations)
- **Goal:** Provide fast, reliable analytic tables for BI reporting.
- **Filtering Rule:** `WHERE is_valid = True` on all Silver input sources.
- **Aggregations:**
  - `gold_sales_by_product`: Product-level revenue, volume, and average order value.
  - `gold_revenue_by_customer`: Customer-level total revenue, order count, and actual LTV.
  - `gold_daily_weekly_trends`: Daily/weekly trend breakdown for executive tracking.
  - `gold_customer_segmentation`: Segmentation cohorts:
    - *High-Value:* Total revenue >= $1,000
    - *Repeat:* Orders > 1 and revenue < $1,000
    - *One-Time:* Orders = 1
    - *Inactive:* Orders = 0

---

## Data Quality & Flagging Strategy

| Layer | Rule Type | Input Field(s) | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Silver** | Completeness | `email`, `customer_id`, `product_id` | Set `is_valid = False`, record `NULL_FOUND` in `quality_check_result` |
| **Silver** | Uniqueness | `customer_id`, `order_id` | Set `is_valid = False`, record `DUPLICATE_KEY` in `quality_check_result` |
| **Silver** | Integrity | `orders.customer_id`, `orders.product_id` | Set `is_valid = False`, record `ORPHAN_FK` in `quality_check_result` |
| **Silver** | Business Logic | `total_amount`, `signup_date` | Set `is_valid = False`, record `INVALID_RANGE` in `quality_check_result` |

---

## Debugging & Error Handling Strategy
- **Schema Drift Protection:** Explicit PySpark StructType schemas enforced during Bronze ingestion.
- **Spark Exception Handling:** Pipeline modules wrapped in structured try/except blocks with explicit logging.
- **Audit Reports:** Data Quality report printed at the end of Silver execution detailing pass/fail counts.
