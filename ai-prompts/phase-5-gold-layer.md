# AI Prompt History — Phase 5: Gold Layer Aggregations

## Prompt 1: Spark SQL Aggregations & Customer Segmentation

**PROMPT SENT:**
```text
Write SQL queries for Gold layer aggregations referencing valid Silver records (is_valid = TRUE):
1. `sales_by_product`: product_id, product_name, category, total_orders, total_revenue, avg_order_value.
2. `revenue_by_customer`: customer_id, customer_name, customer_segment, total_orders, total_revenue, avg_order_value, lifetime_value_actual.
3. `customer_segmentation`: Segment into High-Value (>= $1000), Repeat (>1 order), One-Time (1 order), Inactive (0 orders).
```

**AI RESPONSE SUMMARY:**
- Generated `01_sales_by_product.sql`, `02_revenue_by_customer.sql`, and CTE-based `04_customer_segmentation.sql`.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Clean SQL JOIN and CTE logic filtering out flagged invalid rows (`is_valid = TRUE`).
- **Final Outcome:** Saved in `src/gold/*.sql` and integrated into `src/gold/create_gold_tables.py`.
