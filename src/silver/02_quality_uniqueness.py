#!/usr/bin/env python3
"""
Silver Quality Check 2 — Uniqueness Check (No Duplicate Primary Keys)
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def validate_uniqueness(df: DataFrame, primary_key_cols: list) -> DataFrame:
    """
    Evaluates uniqueness over primary key columns using window functions.
    The first occurrence (ROW_NUMBER = 1) is PASS; duplicates (ROW_NUMBER > 1) are FAIL.
    """
    # Define window over primary keys ordered by ingestion timestamp if available, else literal
    order_col = F.col("_ingested_at") if "_ingested_at" in df.columns else F.lit(1)
    w = Window.partitionBy(*primary_key_cols).orderBy(order_col)
    
    df_rn = df.withColumn("_row_num", F.row_number().over(w))
    
    status_col = F.when(F.col("_row_num") > 1, F.lit(f"FAIL: Duplicate PK [{', '.join(primary_key_cols)}]")) \
                  .otherwise(F.lit("PASS"))
    
    return df_rn.withColumn("uniqueness_status", status_col).drop("_row_num")
