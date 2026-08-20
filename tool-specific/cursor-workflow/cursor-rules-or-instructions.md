# Token-Efficient Cursor AI Rules & Instructions

## Rule Strategy
To optimize AI performance and minimize prompt token usage when developing Databricks Medallion Data Pipelines in Cursor:

1. **Context Economy:** Never paste large raw data files or full log outputs into prompt chats. Reference modular python script paths (`src/silver/01_quality_completeness.py`) using `@file`.
2. **Explicit Contracts:** Define PySpark function signatures before requesting code generation:
   ```python
   def check_completeness(df: DataFrame, mandatory_cols: list) -> DataFrame: ...
   ```
3. **No Redundant Formatting:** Instruct Cursor to skip generic introductory explanations ("Sure, I can help with that...") and output clean Python/SQL implementations directly.
4. **PySpark Best Practices:**
   - Always use `pyspark.sql.functions` aliased as `F`.
   - Avoid `rdd` operations; use PySpark DataFrame expressions or SQL.
   - Use PySpark window functions (`Window.partitionBy()`) for uniqueness checks.
5. **Non-Destructive Tagging Rule:**
   - Always retain raw records in Silver.
   - Add `is_valid` (BOOLEAN) and `quality_check_result` (STRING).
