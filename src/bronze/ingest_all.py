#!/usr/bin/env python3
"""
Bronze Layer Orchestrator — Runs Ingestion for Customers, Products, and Orders
"""

import os
import sys
from pyspark.sql import SparkSession

# Ensure local module imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib

ingest_customers = importlib.import_module("01_ingest_customers").ingest_customers
ingest_orders = importlib.import_module("02_ingest_orders").ingest_orders
ingest_products = importlib.import_module("03_ingest_products").ingest_products

def run_bronze_pipeline(spark, data_dir, warehouse_dir):
    print("=========================================")
    print("STARTING BRONZE LAYER INGESTION PIPELINE")
    print("=========================================")
    
    customers_csv = os.path.join(data_dir, "customers.csv")
    products_csv = os.path.join(data_dir, "products.csv")
    orders_csv = os.path.join(data_dir, "orders.csv")
    
    df_customers = ingest_customers(spark, customers_csv, warehouse_dir)
    df_products = ingest_products(spark, products_csv, warehouse_dir)
    df_orders = ingest_orders(spark, orders_csv, warehouse_dir)
    
    print("\n--- BRONZE INGESTION SUMMARY ---")
    print(f"Bronze Customers: {df_customers.count()} rows")
    print(f"Bronze Products:  {df_products.count()} rows")
    print(f"Bronze Orders:    {df_orders.count()} rows")
    print("=========================================\n")
    
    return df_customers, df_products, df_orders

def get_spark_session(app_name="Bronze_Pipeline_Orchestrator"):
    try:
        from IPython import get_ipython
        ipy = get_ipython()
        if ipy and "spark" in ipy.user_ns:
            return ipy.user_ns["spark"]
    except Exception:
        pass
    try:
        active = SparkSession.getActiveSession()
        if active:
            return active
    except Exception:
        pass
    for k in list(os.environ.keys()):
        if "SPARK_REMOTE" in k or "SPARK_CONNECT" in k or "REMOTE" in k:
            os.environ.pop(k, None)
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.appName(app_name).getOrCreate()
    except Exception:
        pass
    builder = SparkSession.builder.appName(app_name)
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()

if __name__ == "__main__":
    spark = get_spark_session("Bronze_Pipeline_Orchestrator")
    
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
    data_dir = os.path.join(root_dir, "data")
    wh_dir = os.path.join(data_dir, "warehouse")
    
    run_bronze_pipeline(spark, data_dir, wh_dir)
