# Cursor AI Workflow — Project Context

## Project Mission
Build an end-to-end Databricks Medallion Architecture Data Pipeline (Bronze → Silver → Gold → Dashboard) for an e-commerce platform processing daily customers, products, and orders datasets.

## Core Technical Stack
- **Databricks / PySpark:** PySpark DataFrame API for Bronze & Silver; Spark SQL for Gold aggregations & BI queries.
- **Storage:** Delta Lake tables (`delta-spark` local / Databricks Delta format).
- **Python Libraries:** `pyspark`, `pandas`, `faker`, `pytest`.

## Architectural Principles for Cursor
1. **Token Efficiency:** Keep prompt contexts precise. Use `@file` tags when referencing code or docs.
2. **Layer Isolation:**
   - Bronze = Pure ingestion + metadata (`_ingested_at`, `_source_file`).
   - Silver = Data Quality tagging (`is_valid`, `quality_check_result`).
   - Gold = Business aggregations filtered on `is_valid = True`.
3. **No Code Dropping:** Silver checks must tag bad rows, not delete them.
