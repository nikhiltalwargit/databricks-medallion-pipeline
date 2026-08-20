# Data Quality Strategy & Validation Framework

## 1. Data Quality Strategy Overview
Data quality validation is enforced in the **Silver Layer** of the Medallion architecture using a non-destructive tagging paradigm. Rather than discarding bad records immediately, every record is enriched with data quality flags (`is_valid`, `quality_check_result`), enabling downstream audit reporting while guaranteeing that Gold analytics query strictly valid data (`is_valid = True`).

---

## 2. Quality Check Categories & Rules

### Check 1: Completeness
- **Objective:** Ensure mandatory fields contain non-null values.
- **Rules:**
  - `customers.csv`: `customer_id IS NOT NULL AND email IS NOT NULL`
  - `orders.csv`: `order_id IS NOT NULL AND customer_id IS NOT NULL AND product_id IS NOT NULL`
  - `products.csv`: `product_id IS NOT NULL AND price IS NOT NULL`
- **Threshold:** > 99.0% pass rate.
- **Intentional Anomaly Seed:** 50 rows in `customers.csv` with NULL email, 100 rows in `orders.csv` with NULL `customer_id`, 200 rows with NULL `product_id`.

### Check 2: Uniqueness
- **Objective:** Eliminate duplicate primary key records.
- **Rules:**
  - `customers.csv`: `customer_id` must be unique.
  - `orders.csv`: `order_id` must be unique.
  - `products.csv`: `product_id` must be unique.
- **Implementation:** PySpark Windowing (`ROW_NUMBER() OVER (PARTITION BY pk ORDER BY _ingested_at ASC)`).
- **Threshold:** 100% uniqueness required.
- **Intentional Anomaly Seed:** 10 duplicate `customer_id` rows in `customers.csv`, 20 duplicate `order_id` rows in `orders.csv`.

### Check 3: Referential Integrity
- **Objective:** Validate that foreign keys exist in parent dimension tables.
- **Rules:**
  - `orders.customer_id` must exist in `customers.customer_id`.
  - `orders.product_id` must exist in `products.product_id`.
- **Implementation:** PySpark Left Anti-Joins.
- **Threshold:** > 99.9% referential validity.
- **Intentional Anomaly Seed:** 50 orphan `customer_id` rows and 30 orphan `product_id` rows in `orders.csv`.

### Check 4: Business Logic & Type Validation
- **Objective:** Validate domain constraints and valid metric ranges.
- **Rules:**
  - `orders.quantity > 0`
  - `orders.unit_price >= 0`
  - `orders.total_amount >= 0`
  - `customers.signup_date <= CURRENT_DATE()`
- **Threshold:** > 99.9% validity.

---

## 3. Total Intentional Anomaly Inventory

| Source Dataset | Total Rows | Quality Issue Description | Issue Count | Impact % |
| :--- | :--- | :--- | :--- | :--- |
| `customers.csv` | 10,000 | NULL Email | 50 rows | 0.50% |
| `customers.csv` | 10,000 | Duplicate `customer_id` | 10 rows | 0.10% |
| `orders.csv` | 100,000 | NULL `customer_id` | 100 rows | 0.10% |
| `orders.csv` | 100,000 | NULL `product_id` | 200 rows | 0.20% |
| `orders.csv` | 100,000 | Orphan `customer_id` (FK error) | 50 rows | 0.05% |
| `orders.csv` | 100,000 | Orphan `product_id` (FK error) | 30 rows | 0.03% |
| `orders.csv` | 100,000 | Duplicate `order_id` | 20 rows | 0.02% |
| **Total** | **110,500** | **Total Anomaly Count** | **460 rows** | **~0.42%** |

---

## 4. Quality Metrics Reporting Schema
Upon Silver layer completion, a Data Quality Summary Report is logged:

```json
{
  "dataset": "silver_orders",
  "total_records": 100000,
  "valid_records": 99600,
  "invalid_records": 400,
  "overall_pass_rate_pct": 99.60,
  "check_breakdown": {
    "completeness_pass_pct": 99.70,
    "uniqueness_pass_pct": 99.98,
    "referential_integrity_pass_pct": 99.92,
    "business_logic_pass_pct": 100.0
  }
}
```
