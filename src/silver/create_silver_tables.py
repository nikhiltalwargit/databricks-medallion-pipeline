#!/usr/bin/env python3
"""
Silver Layer Orchestrator — Runs Quality Validation Checks and Materializes Silver Tables
"""

import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Ensure local module imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../bronze"))

import importlib

ingest_customers = importlib.import_module("01_ingest_customers").ingest_customers
ingest_orders = importlib.import_module("02_ingest_orders").ingest_orders
ingest_products = importlib.import_module("03_ingest_products").ingest_products

validate_completeness = importlib.import_module("01_quality_completeness").validate_completeness
validate_uniqueness = importlib.import_module("02_quality_uniqueness").validate_uniqueness
validate_types_and_ranges = importlib.import_module("03_quality_type_validation").validate_types_and_ranges
validate_referential_integrity = importlib.import_module("04_quality_referential_integrity").validate_referential_integrity
consolidate_quality_flags = importlib.import_module("05_quality_business_logic").consolidate_quality_flags

def process_silver_customers(spark, df_bronze_cust):
    print("Processing Silver Customers...")
    df_c1 = validate_completeness(df_bronze_cust, ["customer_id", "email"])
    df_c2 = validate_uniqueness(df_c1, ["customer_id"])
    df_c3 = validate_types_and_ranges(df_c2, "customers")
    
    df_silver = consolidate_quality_flags(
        df_c3,
        ["completeness_status", "uniqueness_status", "type_validation_status"]
    )
    df_silver.createOrReplaceTempView("silver_customers")
    return df_silver

def process_silver_products(spark, df_bronze_prod):
    print("Processing Silver Products...")
    df_p1 = validate_completeness(df_bronze_prod, ["product_id", "price"])
    df_p2 = validate_uniqueness(df_p1, ["product_id"])
    df_p3 = validate_types_and_ranges(df_p2, "products")
    
    df_silver = consolidate_quality_flags(
        df_p3,
        ["completeness_status", "uniqueness_status", "type_validation_status"]
    )
    df_silver.createOrReplaceTempView("silver_products")
    return df_silver

def process_silver_orders(spark, df_bronze_orders, df_silver_cust, df_silver_prod):
    print("Processing Silver Orders...")
    df_o1 = validate_completeness(df_bronze_orders, ["order_id", "customer_id", "product_id"])
    df_o2 = validate_uniqueness(df_o1, ["order_id"])
    df_o3 = validate_types_and_ranges(df_o2, "orders")
    df_o4 = validate_referential_integrity(df_o3, df_silver_cust.filter(F.col("is_valid") == True), df_silver_prod.filter(F.col("is_valid") == True))
    
    df_silver = consolidate_quality_flags(
        df_o4,
        ["completeness_status", "uniqueness_status", "type_validation_status", "referential_status"]
    )
    df_silver.createOrReplaceTempView("silver_orders")
    return df_silver

def print_data_quality_report(df_silver, name):
    total = df_silver.count()
    valid = df_silver.filter(F.col("is_valid") == True).count()
    invalid = total - valid
    pass_pct = round((valid / total * 100), 2) if total > 0 else 0.0
    
    print(f"\n=========================================")
    print(f" DATA QUALITY REPORT: {name.upper()}")
    print(f"=========================================")
    print(f" Total Ingested Rows : {total}")
    print(f" Passed (Valid) Rows : {valid}")
    print(f" Flagged (Invalid)  : {invalid}")
    print(f" Quality Pass Rate  : {pass_pct}%")
    print(f"-----------------------------------------")
    print(" Sample Flagged Invalid Records:")
    df_silver.filter(F.col("is_valid") == False).select(df_silver.columns[0], "quality_check_result").show(5, truncate=False)
    print(f"=========================================\n")

def run_silver_pipeline(spark, data_dir, warehouse_dir):
    customers_csv = os.path.join(data_dir, "customers.csv")
    products_csv = os.path.join(data_dir, "products.csv")
    orders_csv = os.path.join(data_dir, "orders.csv")
    
    df_b_cust = ingest_customers(spark, customers_csv)
    df_b_prod = ingest_products(spark, products_csv)
    df_b_orders = ingest_orders(spark, orders_csv)
    
    df_s_cust = process_silver_customers(spark, df_b_cust)
    df_s_prod = process_silver_products(spark, df_b_prod)
    df_s_orders = process_silver_orders(spark, df_b_orders, df_s_cust, df_s_prod)
    
    print_data_quality_report(df_s_cust, "silver_customers")
    print_data_quality_report(df_s_prod, "silver_products")
    print_data_quality_report(df_s_orders, "silver_orders")
    
    if warehouse_dir:
        os.makedirs(warehouse_dir, exist_ok=True)
        df_s_cust.write.mode("overwrite").parquet(os.path.join(warehouse_dir, "silver_customers"))
        df_s_prod.write.mode("overwrite").parquet(os.path.join(warehouse_dir, "silver_products"))
        df_s_orders.write.mode("overwrite").parquet(os.path.join(warehouse_dir, "silver_orders"))
        
    return df_s_cust, df_s_prod, df_s_orders

def get_spark_session(app_name="Silver_Pipeline_Orchestrator"):
    try:
        active = SparkSession.getActiveSession()
        if active:
            return active
    except Exception:
        pass
    try:
        from pyspark.sql.classic.session import SparkSession as ClassicSparkSession
        active_classic = ClassicSparkSession.getActiveSession()
        if active_classic:
            return active_classic
    except Exception:
        pass
    builder = SparkSession.builder.appName(app_name)
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        builder = builder.master("local[*]")
    try:
        return builder.getOrCreate()
    except Exception:
        from pyspark.sql.classic.session import SparkSession as ClassicSparkSession
        return ClassicSparkSession.builder.appName(app_name).getOrCreate()

if __name__ == "__main__":
    spark = get_spark_session("Silver_Pipeline_Orchestrator")
    
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
    data_dir = os.path.join(root_dir, "data")
    wh_dir = os.path.join(data_dir, "warehouse")
    
    run_silver_pipeline(spark, data_dir, wh_dir)
