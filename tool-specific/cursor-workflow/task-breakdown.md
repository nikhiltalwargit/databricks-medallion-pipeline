# Phased Task Breakdown for Cursor Execution

## Phase 1: Foundation & Specs Setup
- [x] Create `.cursorrules` token-optimized rules file.
- [x] Write `candidate-info.md`, `tool-workflow.md`, `requirements-analysis.md`, `design-notes.md`, `data-model.md`, and `data-quality-strategy.md`.
- [x] Log Phase 1 prompt history in `ai-prompts/phase-1-foundation-and-specs.md`.

## Phase 2: Sample Data Generation with Quality Anomalies
- [ ] Implement `src/data_generation/generate_sample_data.py`.
- [ ] Inject ~700 realistic intentional anomalies (50 null emails, 10 duplicate customers, 300 FK errors, 20 duplicate orders).
- [ ] Output `customers.csv` (10k), `orders.csv` (100k), `products.csv` (500).
- [ ] Write `src/data_generation/DATA_GENERATION_NOTES.md` and `ai-prompts/phase-2-data-generation.md`.

## Phase 3: Bronze Layer Ingestion
- [ ] Implement `01_ingest_customers.py`, `02_ingest_orders.py`, `03_ingest_products.py`, and `ingest_all.py`.
- [ ] Enforce PySpark StructType schemas and metadata columns (`_ingested_at`, `_source_file`).
- [ ] Log Phase 3 prompt history in `ai-prompts/phase-3-bronze-layer.md`.

## Phase 4: Silver Layer Data Quality & Cleaning
- [ ] Implement 5 quality check PySpark modules (completeness, uniqueness, type/range, referential integrity, business logic).
- [ ] Implement non-destructive tagging (`is_valid`, `quality_check_result`).
- [ ] Build `create_silver_tables.py` and log Data Quality Summary Report.
- [ ] Log Phase 4 prompt history in `ai-prompts/phase-4-silver-layer.md`.

## Phase 5: Gold Layer Aggregations
- [ ] Implement `01_sales_by_product.sql`, `02_revenue_by_customer.sql`, `03_daily_weekly_trends.sql`, `04_customer_segmentation.sql`, and `create_gold_tables.py`.
- [ ] Materialize Gold Delta tables filtering on `is_valid = True`.
- [ ] Log Phase 5 prompt history in `ai-prompts/phase-5-gold-layer.md`.

## Phase 6: Dashboard Queries & Visualizations
- [ ] Implement `src/dashboard/dashboard_queries.sql` (4 SQL visualization queries).
- [ ] Write `src/dashboard/DASHBOARD_GUIDE.md`.
- [ ] Log Phase 6 prompt history in `ai-prompts/phase-6-dashboard-and-bi.md`.

## Phase 7: Testing, Debugging, Databricks Deployment & Reflection
- [ ] Implement PyTest suite (`test_data_generation.py`, `test_silver_quality_checks.py`, `test_gold_aggregations.py`).
- [ ] Write `database/schema.sql`, `database/seed-data-notes.md`, `database/setup-notes.md`.
- [ ] Write `debugging-notes.md`, `reflection.md`, `final-ai-usage-summary.md`, and Databricks-ready `README.md`.
- [ ] Log Phase 7 prompt history in `ai-prompts/phase-7-testing-and-debugging.md`.
