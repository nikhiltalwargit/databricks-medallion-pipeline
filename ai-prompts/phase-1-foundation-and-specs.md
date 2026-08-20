# AI Prompt History — Phase 1: Foundation & Technical Specs

## Prompt 1: Project Architecture & Medallion Strategy Setup

**PROMPT SENT:**
```text
I am building an e-commerce Medallion architecture data pipeline (Bronze -> Silver -> Gold) on Databricks using PySpark.
Help me outline the requirements analysis and design notes.
We need:
1. Raw CSV ingestion into Bronze Delta tables with metadata (_ingested_at, _source_file).
2. Non-destructive Silver validation tagging (is_valid boolean, quality_check_result JSON).
3. Gold aggregations (sales by product, revenue by customer, daily/weekly trends, customer segmentation).
4. Databricks SQL dashboard queries.
Keep the design clean, modular, and token-efficient.
```

**AI RESPONSE SUMMARY:**
- Outlined 3-tier architecture with raw CSV landing in Bronze.
- Defined non-destructive Silver layer tagging model using PySparkStruct/JSON fields.
- Proposed 4 Gold aggregate views and 4 SQL queries for BI visualization.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Layer separation, metadata columns, and non-destructive tagging approach.
- ⚡ **Adjusted:** Ensured customer segmentation logic includes explicit thresholds ($1,000+ for High-Value, >1 order for Repeat, 1 order for One-Time, 0 orders for Inactive).
- **Final Outcome:** Saved into `requirements-analysis.md` and `design-notes.md`.

---

## Prompt 2: Token-Optimized Rules (.cursorrules) Configuration

**PROMPT SENT:**
```text
Create a concise .cursorrules file for Databricks PySpark and Delta Lake development.
Requirements:
- Emphasize modular PySpark code using F.col / F.when functions.
- Mandate non-destructive data quality tagging in Silver.
- Enforce token-efficient outputs: direct python/sql implementations without unnecessary fluff.
```

**AI RESPONSE SUMMARY:**
- Generated clean `.cursorrules` file specifying core principles, Databricks Delta Lake standards, and code guidelines.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Complete adoption. Saved to `.cursorrules` and `tool-specific/cursor-workflow/cursor-rules-or-instructions.md`.
