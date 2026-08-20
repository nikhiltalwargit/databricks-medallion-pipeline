#!/usr/bin/env python3
"""
Silver Quality Check 4 — Referential Integrity Check (Foreign Key Validation)
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def validate_referential_integrity(df_orders: DataFrame, df_customers: DataFrame, df_products: DataFrame) -> DataFrame:
    """
    Validates foreign key references in orders table against valid primary keys in customers and products.
    Adds `referential_status`.
    """
    # Distinct valid primary keys
    cust_pks = df_customers.select("customer_id").distinct().filter(F.col("customer_id").isNotNull())
    prod_pks = df_products.select("product_id").distinct().filter(F.col("product_id").isNotNull())
    
    # Broadcast or alias joins
    orders_alias = df_orders.alias("o")
    
    joined = orders_alias.join(cust_pks.alias("c"), F.col("o.customer_id") == F.col("c.customer_id"), "left") \
                         .join(prod_pks.alias("p"), F.col("o.product_id") == F.col("p.product_id"), "left")
    
    invalid_cust = F.col("o.customer_id").isNotNull() & F.col("c.customer_id").isNull()
    invalid_prod = F.col("o.product_id").isNotNull() & F.col("p.product_id").isNull()
    
    ref_status = F.when(invalid_cust & invalid_prod, F.lit("FAIL: Orphan customer_id & product_id")) \
                  .when(invalid_cust, F.lit("FAIL: Orphan customer_id")) \
                  .when(invalid_prod, F.lit("FAIL: Orphan product_id")) \
                  .otherwise(F.lit("PASS"))
    
    result_df = joined.select("o.*", ref_status.alias("referential_status"))
    return result_df
