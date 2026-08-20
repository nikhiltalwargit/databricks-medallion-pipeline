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

if __name__ == "__main__":
    spark = (SparkSession.builder
             .appName("Bronze_Pipeline_Orchestrator")
             .master("local[*]")
             .getOrCreate())
    
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
    data_dir = os.path.join(root_dir, "data")
    wh_dir = os.path.join(data_dir, "warehouse")
    
    run_bronze_pipeline(spark, data_dir, wh_dir)
