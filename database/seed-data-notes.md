# Seed Data & Data Loading Notes

## Sample Raw Files Location
- Local Workspace: `data/customers.csv`, `data/orders.csv`, `data/products.csv`
- Databricks DBFS / S3 Landing Path: `dbfs:/FileStore/tables/ecommerce/` or `s3://<my-bucket>/landing/`

## Raw CSV Specifications & Row Counts
1. **`customers.csv`**: 10,010 rows (~500 KB) — 10,000 base + 10 duplicate customer IDs + 50 NULL emails.
2. **`orders.csv`**: 100,020 rows (~3.2 MB) — 100,000 base + 20 duplicate order IDs + 100 NULL customer IDs + 200 NULL product IDs + 50 orphan customer IDs + 30 orphan product IDs.
3. **`products.csv`**: 500 rows (~50 KB) — 500 clean base products across 7 categories.

## Loading into Databricks Repos
1. Clone this repository into Databricks Repos via Git (`https://github.com/<your-username>/databricks-medallion-pipeline.git`).
2. Run `src/data_generation/generate_sample_data.py` to generate or refresh raw CSV files in DBFS/local path.
