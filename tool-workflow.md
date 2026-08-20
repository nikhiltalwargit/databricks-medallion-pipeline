# Part A: AI Workflow Foundation — Tool & Process Guide

## 1. Primary AI Tool Used
- **Tool:** Cursor IDE (integrating Claude 3.5 Sonnet & GPT-4o models).
- **Configuration:** Project-level `.cursorrules` file configured for token efficiency, strict PySpark/Databricks standards, and modular data pipeline design patterns.

## 2. Providing Project Context to AI
- **Context Anchor Files:** Dedicated context files under `tool-specific/cursor-workflow/` (`project-context.md`, `spec.md`, `task-breakdown.md`) serve as persistent knowledge bases.
- **Symbol & File Tagging:** Precise `@file` and `@symbol` references used in Cursor prompts to keep input tokens lean and targeted rather than pasting entire repositories.

## 3. AI for Requirement Analysis
- **Workflow:** Deconstructed business goals into functional requirements, non-functional requirements, data schema constraints, and edge cases.
- **Technique:** Prompted AI to critique architectural assumptions, identify missing data quality constraints, and outline edge-case anomalies (e.g., handling null keys, orphan orders, timezone shifts).

## 4. AI for Medallion Pipeline Design
- **Bronze Layer (Raw):** AI assisted in defining raw table schemas, schema evolution parameters, and metadata columns (`_ingested_at`, `_source_file`).
- **Silver Layer (Cleaned & Validated):** Designed non-destructive data quality tagging using JSON struct flags (`quality_check_result`) and boolean validity markers (`is_valid`).
- **Gold Layer (Aggregated):** Engineered business aggregation models (Sales by Product, Revenue by Customer, Customer Segmentation) using modular PySpark and standard Spark SQL syntax.

## 5. AI for Code Generation (Python / PySpark / SQL)
- **Prompt Strategy:** Structured, single-responsibility prompts ("Write pure PySpark function to check referential integrity between orders and customers").
- **Token Efficiency:** Leveraged `.cursorrules` to instruct AI to output functional code without repetitive preamble or excessive commentary.

## 6. Code & Logic Validation Workflow
- **Static Analysis & Linting:** Verified syntax against standard PySpark APIs.
- **Execution Verification:** Tested all generated scripts against PySpark local runtime and Databricks Delta Lake engines.
- **Logic Inspection:** Manually reviewed window functions, joins, and filter conditions to ensure non-valid rows were properly flagged rather than accidentally dropped in Silver.

## 7. AI for Testing & Test Suite Generation
- **Pytest Suite:** Used AI to scaffold unit test fixtures with synthetic PySpark DataFrames containing known passing and failing records.
- **Assertion Verification:** Verified that test assertions accurately assert expected counts of flagged rows (50 null emails, 10 duplicate customers, 300 orphan FKs, etc.).

## 8. AI for Debugging & Troubleshooting
- **Methodology:** Pasted exact PySpark execution stack traces into Cursor with high-context prompt snippets.
- **Root-Cause Analysis:** Leveraged AI to identify DataFrame schema mismatches, nullability conflicts in Delta tables, and Spark column alias shadowing.

## 9. AI for Data Quality Strategy
- **Rule Formulation:** Co-designed the 4 core quality check categories: Completeness, Uniqueness, Referential Integrity, and Type/Business Validation.
- **Metrics Reporting:** Prompted AI to build dynamic aggregate queries summarizing pass/fail percentages across each dataset and rule set.

## 10. Security & PII Protection Policy
- **Synthetic Data Usage:** Synthetic mock data generated exclusively via Python `faker` library.
- **PII Safeguards:** Zero real customer data, credentials, API keys, or sensitive internal schemas submitted to AI prompts.
- **Rule:** Sanitized all log outputs and stack traces before prompt inclusion.

## 11. Production Workflow Reusability
- **CI/CD Integration:** Workflow translates directly into production Databricks pipelines (Databricks Workflows / Asset Bundles).
- **Reusable Templates:** Prompt templates and `.cursorrules` saved in the repo can be reused across all competency data projects.

## 12. Lessons Learned & Retrospective
- **What Worked Well:** Phased prompt breakdown, token-optimized rules, non-destructive Silver layer tagging, automated PyTest suite.
- **What Didn't Work:** Vague one-liner prompts ("generate medallion pipeline") produced over-engineered code with missing edge cases. Specific, iterative prompts yielded 10x better results.
