# AI Prompt History — Phase 2: Sample Data Generation

## Prompt 1: Customer Data Generation Script with Quality Issues

**PROMPT SENT:**
```text
Write a standalone Python script to generate realistic customer CSV data.
Needs 10,000 customers with fields: customer_id (INT), customer_name (STRING), email (STRING), country (STRING), signup_date (DATE 2020-2025), customer_segment (Basic/Standard/Premium), lifetime_value (DECIMAL).
Inject these data quality issues for testing:
- 50 rows with empty/NULL email
- 10 duplicate customer_id rows
Make it deterministic using random.seed(42).
```

**AI RESPONSE SUMMARY:**
- Provided Python script using standard `csv`, `random`, and `datetime` libraries.
- Implemented `generate_customers` with exact requested schema and anomaly injection.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Code design, seed configuration, and dictionary writer.
- ⚡ **Adjusted:** Added explicit logging of final generated file row counts.
- **Final Decision:** Integrated into `generate_sample_data.py`.

---

## Prompt 2: Orders Dataset Generation with Multi-Column Anomalies

**PROMPT SENT:**
```text
Extend the python data generator to produce 100,000 order CSV records referencing valid customer_ids and product_ids.
Schema: order_id, customer_id, order_date, product_id, quantity, unit_price, total_amount, order_status, payment_date.
Inject these quality anomalies:
- 100 rows with NULL customer_id
- 200 rows with NULL product_id
- 50 orphan customer_ids (e.g. 999001..999050)
- 30 orphan product_ids (e.g. 888001..888030)
- 20 duplicate order_ids
```

**AI RESPONSE SUMMARY:**
- Generated `generate_orders` function taking `valid_cids` and `valid_pids` as inputs.
- Implemented sample-based indexing to inject completeness, referential integrity, and uniqueness errors cleanly.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Perfect match for intentional quality anomaly testing.
- **Final Outcome:** Saved script in `src/data_generation/generate_sample_data.py` and executed to produce raw datasets in `data/`.
