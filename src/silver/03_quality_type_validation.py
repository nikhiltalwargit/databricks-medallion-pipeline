#!/usr/bin/env python3
"""
Silver Quality Check 3 — Type & Range Validation
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def validate_types_and_ranges(df: DataFrame, table_type: str) -> DataFrame:
    """
    Validates numeric ranges and date boundaries based on dataset type.
    Adds `type_validation_status`.
    """
    if table_type == "orders":
        invalid_cond = (F.col("quantity") <= 0) | \
                       (F.col("unit_price") < 0) | \
                       (F.col("total_amount") < 0)
        status_col = F.when(invalid_cond, F.lit("FAIL: Invalid quantity/price range")).otherwise(F.lit("PASS"))
    elif table_type == "customers":
        invalid_cond = (F.col("signup_date") > F.current_date()) | \
                       (F.col("lifetime_value") < 0)
        status_col = F.when(invalid_cond, F.lit("FAIL: Invalid signup date or LTV")).otherwise(F.lit("PASS"))
    elif table_type == "products":
        invalid_cond = (F.col("price") < 0) | (F.col("cost") < 0)
        status_col = F.when(invalid_cond, F.lit("FAIL: Negative price/cost")).otherwise(F.lit("PASS"))
    else:
        status_col = F.lit("PASS")
        
    return df.withColumn("type_validation_status", status_col)
