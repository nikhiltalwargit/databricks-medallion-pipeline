# AI Prompt History — Phase 4: Silver Layer Data Quality & Cleaning

## Prompt 1: Completeness & Uniqueness Validation Modules

**PROMPT SENT:**
```text
Write modular PySpark data quality functions:
1. `validate_completeness(df, mandatory_cols)` checking for NULL or empty strings.
2. `validate_uniqueness(df, primary_keys)` using Window functions. The first occurrence is PASS, duplicates are tagged FAIL.
Ensure bad rows are tagged, NOT deleted.
```

**AI RESPONSE SUMMARY:**
- Created PySpark functions adding `completeness_status` and `uniqueness_status` string columns.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Preserves bad rows for auditing while isolating failure reasons.
- **Final Outcome:** Saved into `src/silver/01_quality_completeness.py` and `src/silver/02_quality_uniqueness.py`.

---

## Prompt 2: Referential Integrity & Quality Consolidation

**PROMPT SENT:**
```text
Write PySpark modules for:
1. `validate_referential_integrity(orders_df, cust_df, prod_df)` doing left-anti checks against parent keys.
2. `consolidate_quality_flags(df, check_cols)` producing:
   - `is_valid` (BOOLEAN: True if ALL checks PASS, False otherwise)
   - `quality_check_result` (JSON struct of individual check outcomes)
```

**AI RESPONSE SUMMARY:**
- Provided referential integrity module checking orphan `customer_id` and `product_id` keys in orders, and consolidator function aggregating flags into JSON struct.

**EVALUATION & DECISION LOG:**
- ✓ **Accepted:** Clean JSON struct auditing pattern.
- **Final Outcome:** Saved into `src/silver/04_quality_referential_integrity.py` and `src/silver/05_quality_business_logic.py`.
