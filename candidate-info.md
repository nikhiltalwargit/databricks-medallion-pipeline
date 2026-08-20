# Candidate Information

**Name:** Data Engineering Participant  
**Role:** Senior Data Engineer / Tech Lead Candidate  
**Primary Technology Stack:** Python / PySpark, SQL, Databricks, Delta Lake  
**Primary AI Tool Used:** Cursor (with Claude 3.5 Sonnet / GPT-4o backend)  
**Project Option Selected:** Data Pipeline (Medallion Architecture — Bronze → Silver → Gold → Dashboard)  
**Assessment Start Date:** 2026-08-21  
**Submission Date:** 2026-08-21  

## Tools & Environment
- **Databricks Environment:** Databricks Community Edition / Workspace Repos & Local PySpark (Delta Lake 3.x)
- **Languages:** Python 3.10+, PySpark 3.5+, SQL
- **Libraries:** PySpark, Delta Lake (`delta-spark`), pandas, faker, pytest
- **AI Tools & Workflow:** Cursor IDE, `.cursorrules` (token-optimized), phased prompt history tracking

## Setup Summary
1. **Repository Link:** Public GitHub repository cloneable directly into Databricks Repos or local workspace.
2. **Execution Steps:**
   - Run sample data generator: `python src/data_generation/generate_sample_data.py`
   - Run Bronze ingestion: `python src/bronze/ingest_all.py`
   - Run Silver validation & DQ report: `python src/silver/create_silver_tables.py`
   - Run Gold aggregations: `python src/gold/create_gold_tables.py`
   - Run Automated Test Suite: `pytest tests/`
