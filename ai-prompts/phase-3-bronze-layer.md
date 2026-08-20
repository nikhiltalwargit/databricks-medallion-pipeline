# AI Prompt History — Phase 3: Bronze Layer Ingestion

## Prompt 1: PySpark Schema Enforcement & Ingestion Modules

**PROMPT SENT:**
```text
Write modular PySpark ingestion scripts for customers.csv, orders.csv, and products.csv.
Requirements:
- Define explicit PySpark StructType schemas.
- Enrich every row with metadata columns: _ingested_at (TIMESTAMP) and _source_file (STRING).
- Support writing outputs as Parquet / Delta files and creating Spark temporary views (bronze_customers, bronze_orders, bronze_products).
```

**AI RESPONSE SUMMARY:**
- Created `01_ingest_customers.py`, `02_ingest_orders.py`, and `03_ingest_products.py` with StructType definitions and metadata enrichment via `F.current_timestamp()` and `F.lit()`.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Explicit schema enforcement prevents schema drift.
- ⚡ **Adjusted:** Added fallback support for local execution when Delta Spark extension is absent in base local Python environments.

---

## Prompt 2: Bronze Orchestration Script

**PROMPT SENT:**
```text
Create ingest_all.py to run all three Bronze ingestion jobs sequentially and print a clean row count summary report.
```

**AI RESPONSE SUMMARY:**
- Generated `run_bronze_pipeline` function executing ingestion modules for customers, products, and orders, logging total counts.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Clear logging and return signatures.
- **Final Outcome:** Saved in `src/bronze/ingest_all.py`.
