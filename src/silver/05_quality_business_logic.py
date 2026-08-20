#!/usr/bin/env python3
"""
Silver Quality Check 5 — Business Rules Engine & Non-Destructive Flag Summarizer
"""

import json
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def consolidate_quality_flags(df: DataFrame, check_cols: list) -> DataFrame:
    """
    Combines individual check status columns into a unified `is_valid` boolean flag
    and a structured JSON string `quality_check_result`.
    """
    # Determine overall validity: True if all check columns equal 'PASS'
    valid_conditions = [F.col(c) == "PASS" for c in check_cols if c in df.columns]
    
    if valid_conditions:
        is_valid_col = valid_conditions[0]
        for cond in valid_conditions[1:]:
            is_valid_col = is_valid_col & cond
    else:
        is_valid_col = F.lit(True)
        
    # Construct JSON struct of check results
    struct_pairs = []
    for c in check_cols:
        if c in df.columns:
            struct_pairs.extend([F.lit(c.replace("_status", "")), F.col(c)])
            
    json_result_col = F.to_json(F.struct(*struct_pairs))
    
    df_consolidated = df.withColumn("is_valid", is_valid_col) \
                        .withColumn("quality_check_result", json_result_col)
                        
    # Drop transient check status columns
    for c in check_cols:
        if c in df.columns:
            df_consolidated = df_consolidated.drop(c)
            
    return df_consolidated
