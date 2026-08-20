# Reflection & AI Workflow Retrospective

## What I Built
I engineered a production-grade, 3-tier Databricks Medallion Architecture Data Pipeline (Bronze → Silver → Gold → BI Dashboard) using PySpark, Delta Lake, and SQL. The pipeline ingests 110,000+ raw e-commerce records, enforces 4 data quality validation tiers non-destructively, generates business aggregations, and serves executive BI dashboard queries.

## How I Used AI (Across the Lifecycle)
- **Phase 1 (Design & Specs):** Used Cursor AI to critique architectural trade-offs between hard-deleting invalid records vs. non-destructive JSON tagging in Silver.
- **Phase 2 (Data Generation):** Prompted AI to generate synthetic sample datasets with deterministic seeds (`random.seed(42)`) and ~460 intentional quality anomalies.
- **Phase 3 (Bronze Ingestion):** Scaffolding PySpark schema enforcement and metadata auditing columns (`_ingested_at`, `_source_file`).
- **Phase 4 (Silver Validation):** Co-designed PySpark quality validation functions (completeness, uniqueness, referential integrity) returning boolean flags (`is_valid`) and failure audit JSON structs (`quality_check_result`).
- **Phase 5 (Gold Aggregations):** Formulated optimized Spark SQL aggregations for product sales, customer revenue, and customer segmentation cohorts.
- **Phase 6 & 7 (Dashboard & Testing):** Scaffolded automated PyTest test suites and BI visualization queries.

## What AI Helped With Most
- **Scaffolding Repetitive Boilerplate:** Rapidly generated PySpark StructType schemas and PyTest fixtures.
- **Root Cause Diagnostics:** Diagnosed Spark ambiguous column name exceptions during referential integrity joins in seconds.
- **Token-Optimized Rule Setting:** Leveraging `.cursorrules` ensured lean, high-signal code suggestions without conversational fluff.

## What AI Got Wrong & How I Fixed It
- **Attempted Hard Deletions in Silver:** Initially, AI generated code filtering out invalid records immediately in Silver. I rejected this and instructed AI to use non-destructive tagging (`is_valid = False` + `quality_check_result`), preserving bad records for downstream auditing.
- **Ambiguous Column Name Shadowing:** AI wrote `df_orders.join(df_customers, "customer_id")` which caused column reference errors in downstream transforms. I refactored it to use explicit DataFrame aliases (`orders.alias("o")`).

## What I Would Improve Next
- **Delta Lake Change Data Feed (CDF):** Enable Delta CDF on Silver tables for incremental streaming updates to Gold aggregations.
- **Great Expectations Integration:** Complement custom PySpark quality functions with Great Expectations for enterprise-wide data contracts.
- **Databricks Asset Bundles (DABs):** Package the pipeline into DAB YAML manifests for automated CI/CD deployments via GitHub Actions.
