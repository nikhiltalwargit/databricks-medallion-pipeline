# Databricks Medallion Architecture Data Pipeline — AI Capability Exercise

[![Databricks](https://img.shields.io/badge/Databricks-Supported-orange?logo=databricks)](https://databricks.com/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-yellow?logo=apachespark)](https://spark.apache.org/)
[![Delta Lake](https://img.shields.io/badge/Delta_Lake-3.x-blue)](https://delta.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![PyTest](https://img.shields.io/badge/PyTest-Passing-green?logo=pytest)](https://docs.pytest.org/)

An end-to-end, production-grade Databricks Medallion Architecture Data Pipeline (Bronze → Silver → Gold → Dashboard) built with AI-assisted engineering practices (Cursor IDE, `.cursorrules`, token-optimized workflow).

---

## 🏗️ Architecture Overview

```
[ Landing Raw CSVs ]  (customers.csv, orders.csv, products.csv)
          │
          ▼
   [ BRONZE LAYER ]   ── Ingest raw data into Delta tables + append metadata
          │              (bronze_customers, bronze_orders, bronze_products)
          │              Adds `_ingested_at` timestamp & `_source_file`
          ▼
   [ SILVER LAYER ]   ── Data Quality Engine (Non-destructive flagging)
          │              (silver_customers, silver_orders, silver_products)
          │              Appends `is_valid` (BOOLEAN) & `quality_check_result` (JSON)
          ▼
    [ GOLD LAYER ]    ── Business Aggregations (Only `is_valid = True` records)
          │              (gold_sales_by_product, gold_revenue_by_customer,
          │               gold_customer_segmentation)
          ▼
  [ BI DASHBOARDS ]   ── Databricks SQL Visualization Queries
```

---

## 📁 Repository Structure

```
databricks-medallion-pipeline/
├── .cursorrules                               # Token-optimized AI rules for Cursor
├── .gitignore                                 # Public GitHub repository rules
├── README.md                                  # End-to-end setup and architecture guide
├── candidate-info.md                          # Candidate & Environment information
├── tool-workflow.md                           # Part A: AI Workflow Foundation Details
├── requirements-analysis.md                   # Problem breakdown & functional requirements
├── design-notes.md                            # Medallion design & technical architecture
├── data-model.md                              # Entity Relationship & Schema specs
├── data-quality-strategy.md                   # DQ checks & intentional anomaly inventory
├── debugging-notes.md                         # Log analysis & error resolution history
├── reflection.md                              # AI workflow retrospective
├── final-ai-usage-summary.md                  # Executive AI usage report
│
├── tool-specific/
│   └── cursor-workflow/
│       ├── project-context.md                # AI persistent context definition
│       ├── spec.md                           # Pipeline specification
│       ├── cursor-rules-or-instructions.md   # Token-efficient AI rules guide
│       └── task-breakdown.md                 # Phased execution checklist
│
├── src/
│   ├── data_generation/
│   │   ├── generate_sample_data.py            # Generates CSVs with ~700 intentional anomalies
│   │   └── DATA_GENERATION_NOTES.md
│   ├── bronze/
│   │   ├── 01_ingest_customers.py
│   │   ├── 02_ingest_orders.py
│   │   ├── 03_ingest_products.py
│   │   └── ingest_all.py                      # Bronze layer orchestrator
│   ├── silver/
│   │   ├── 01_quality_completeness.py
│   │   ├── 02_quality_uniqueness.py
│   │   ├── 03_quality_type_validation.py
│   │   ├── 04_quality_referential_integrity.py
│   │   ├── 05_quality_business_logic.py
│   │   └── create_silver_tables.py            # Silver layer orchestrator & DQ reporter
│   ├── gold/
│   │   ├── 01_sales_by_product.sql
│   │   ├── 02_revenue_by_customer.sql
│   │   ├── 03_daily_weekly_trends.sql
│   │   ├── 04_customer_segmentation.sql
│   │   └── create_gold_tables.py              # Gold layer orchestrator
│   └── dashboard/
│       ├── dashboard_queries.sql              # 4 Databricks SQL visualization queries
│       └── DASHBOARD_GUIDE.md                 # BI layout & setup guide
│
├── data/                                      # Sample CSV datasets
│   ├── customers.csv                          # 10,010 rows (50 NULL emails, 10 duplicate IDs)
│   ├── orders.csv                             # 100,020 rows (~630 NULLs/referential errors)
│   └── products.csv                           # 500 rows
│
├── database/
│   ├── schema.sql                             # DDL for Lakehouse tables
│   ├── seed-data-notes.md                     # Seed data specifications
│   └── setup-notes.md                         # Databricks Repos & local deployment guide
│
├── ai-prompts/                                # Phased prompt logs (Human-style developer logs)
│   ├── phase-1-foundation-and-specs.md
│   ├── phase-2-data-generation.md
│   ├── phase-3-bronze-layer.md
│   ├── phase-4-silver-layer.md
│   ├── phase-5-gold-layer.md
│   ├── phase-6-dashboard-and-bi.md
│   └── phase-7-testing-and-debugging.md
│
└── tests/                                     # Automated PyTest test suite
    ├── test_data_generation.py
    ├── test_silver_quality_checks.py
    └── test_gold_aggregations.py
```

---

## 🚀 Quick Start Guide

### Option 1: Databricks Repos (Recommended for Databricks Users)
1. In your Databricks Workspace, go to **Repos** -> **Add Repo**.
2. Paste the public GitHub URL: `https://github.com/<your-username>/databricks-medallion-pipeline.git`.
3. Execute table creation DDL in Databricks SQL:
   ```sql
   RUN FILE "./database/schema.sql";
   ```
4. Execute the medallion pipeline scripts step-by-step using notebook cells:
   - **Cell 1 (Data Generation):** `!python ./src/data_generation/generate_sample_data.py`
   - **Cell 2 (Bronze Ingestion):** `!python ./src/bronze/ingest_all.py`
   - **Cell 3 (Silver DQ Validation):** `!python ./src/silver/create_silver_tables.py`
   - **Cell 4 (Gold Aggregations):** `!python ./src/gold/create_gold_tables.py`

### Option 2: Local PySpark Execution
1. Clone repository and install dependencies:
   ```bash
   git clone https://github.com/<your-username>/databricks-medallion-pipeline.git
   cd databricks-medallion-pipeline
   pip install pyspark delta-spark pytest pandas faker
   ```
2. Generate sample data with intentional anomalies:
   ```bash
   python3 src/data_generation/generate_sample_data.py
   ```
3. Run Bronze, Silver, and Gold pipeline layers:
   ```bash
   python3 src/bronze/ingest_all.py
   python3 src/silver/create_silver_tables.py
   python3 src/gold/create_gold_tables.py
   ```
4. Run automated test suite:
   ```bash
   pytest tests/
   ```

---

## 📊 Data Quality Engine & Anomaly Inventory

The pipeline implements **non-destructive data quality tagging** in the Silver Layer. Every record is evaluated across 4 dimensions, appending an `is_valid` boolean flag and a `quality_check_result` JSON struct. Bad records are preserved for auditing while Gold aggregations query strictly `is_valid = True`.

| Dataset | Total Rows | Quality Issue Category | Anomaly Seed Description | Total Anomaly Count |
| :--- | :--- | :--- | :--- | :--- |
| `customers.csv` | 10,010 | Completeness | NULL / Empty `email` | 50 rows |
| `customers.csv` | 10,010 | Uniqueness | Duplicate `customer_id` | 10 rows |
| `orders.csv` | 100,020 | Completeness | NULL `customer_id` / NULL `product_id` | 300 rows |
| `orders.csv` | 100,020 | Referential Integrity | Orphan `customer_id` (FK error) | 50 rows |
| `orders.csv` | 100,020 | Referential Integrity | Orphan `product_id` (FK error) | 30 rows |
| `orders.csv` | 100,020 | Uniqueness | Duplicate `order_id` | 20 rows |
| **Total** | **110,530** | **All Categories** | **Total Quality Anomalies** | **~460 rows (~0.42%)** |

---

## 📈 BI Dashboard Visualizations

Four Databricks SQL visualization queries are provided in `src/dashboard/dashboard_queries.sql`:
1. **Top 10 Products by Revenue** (Bar Chart)
2. **Customer Revenue Distribution Tiers** (Column Histogram)
3. **Customer Segmentation Share** (Donut / Pie Chart)
4. **Weekly Revenue Trend** (Line Chart)

---

## 🤖 AI Capability & Prompt History

Prompt history is logged phase-by-phase under `ai-prompts/phase-*.md`. Every prompt log captures:
- Exact human prompt sent
- AI response summary
- Evaluation & Decision Log (accepted, adjusted, rejected reasons)
- Token-optimized rule enforcement via `.cursorrules`
