#!/usr/bin/env python3
"""
Silver Quality Check 1 — Completeness Check (No NULLs in Critical Fields)
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def validate_completeness(df: DataFrame, mandatory_columns: list) -> DataFrame:
    """
    Evaluates nullability across mandatory fields.
    Adds a `completeness_status` column ('PASS' or 'FAIL: NULL in <col>').
    """
    null_conditions = []
    for col_name in mandatory_columns:
        null_conditions.append(
            F.when(F.col(col_name).isNull() | (F.trim(F.col(col_name).cast("string")) == ""), F.lit(col_name))
        )
    
    # Concatenate missing column names if any
    missing_cols = F.concat_ws(", ", *null_conditions)
    
    status_col = F.when(missing_cols != "", F.concat(F.lit("FAIL: NULL in ["), missing_cols, F.lit("]"))) \
                  .otherwise(F.lit("PASS"))
    
    return df.withColumn("completeness_status", status_col)
