# Databricks Environment Setup Notes

## Prerequisites
- Databricks Community Edition or Standard/Premium Workspace (Runtime 13.3 LTS or 14.3 LTS).
- Python 3.10+ and PySpark 3.4+.

## Option A: Running via Databricks Repos
1. Log into your Databricks workspace.
2. Go to **Workspace** -> **Repos** -> **Add Repo**.
3. Enter your GitHub public repository URL (e.g. `https://github.com/<your-username>/databricks-medallion-pipeline.git`).
4. Open notebook or cluster terminal and run `database/schema.sql` to initialize the Delta Lake database:
   ```sql
   %sql
   RUN FILE "./database/schema.sql";
   ```
5. Execute the medallion pipeline scripts step-by-step using notebook cells:
   - **Cell 1 (Data Generation):** `!python ./src/data_generation/generate_sample_data.py`
   - **Cell 2 (Bronze Ingestion):** `!python ./src/bronze/ingest_all.py`
   - **Cell 3 (Silver DQ Validation):** `!python ./src/silver/create_silver_tables.py`
   - **Cell 4 (Gold Aggregations):** `!python ./src/gold/create_gold_tables.py`

## Option B: Standalone Local PySpark Execution
1. Clone repository locally.
2. Install Python requirements:
   ```bash
   pip install pyspark delta-spark pytest pandas faker
   ```
3. Execute pipeline end-to-end:
   ```bash
   python3 src/data_generation/generate_sample_data.py
   python3 src/bronze/ingest_all.py
   python3 src/silver/create_silver_tables.py
   python3 src/gold/create_gold_tables.py
   pytest tests/
   ```
