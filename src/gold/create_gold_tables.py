#!/usr/bin/env python3
"""
Gold Layer Orchestrator — Materializes Gold Aggregate Tables from Silver Layer Data
"""

import os
import sys
from pyspark.sql import SparkSession

# Ensure local module imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../silver"))

from create_silver_tables import run_silver_pipeline

def run_gold_pipeline(spark, data_dir, warehouse_dir):
    print("=========================================")
    print("STARTING GOLD LAYER AGGREGATION PIPELINE")
    print("=========================================")
    
    # 1. Execute Silver Pipeline to load valid Silver temporary views
    df_s_cust, df_s_prod, df_s_orders = run_silver_pipeline(spark, data_dir, warehouse_dir)
    
    gold_dir = os.path.join(warehouse_dir, "gold")
    os.makedirs(gold_dir, exist_ok=True)
    
    # 2. Build Gold Sales by Product
    sql_product = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.total_amount), 2) AS total_revenue,
            ROUND(AVG(o.total_amount), 2) AS avg_order_value
        FROM silver_orders o
        JOIN silver_products p ON o.product_id = p.product_id
        WHERE o.is_valid = TRUE AND p.is_valid = TRUE
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_revenue DESC
    """
    df_gold_product = spark.sql(sql_product)
    df_gold_product.createOrReplaceTempView("gold_sales_by_product")
    df_gold_product.write.mode("overwrite").parquet(os.path.join(gold_dir, "gold_sales_by_product"))
    
    # 3. Build Gold Revenue by Customer
    sql_customer = """
        SELECT 
            c.customer_id,
            c.customer_name,
            c.customer_segment,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.total_amount), 2) AS total_revenue,
            ROUND(AVG(o.total_amount), 2) AS avg_order_value,
            ROUND(SUM(o.total_amount), 2) AS lifetime_value_actual
        FROM silver_customers c
        JOIN silver_orders o ON c.customer_id = o.customer_id
        WHERE c.is_valid = TRUE AND o.is_valid = TRUE
        GROUP BY c.customer_id, c.customer_name, c.customer_segment
        ORDER BY total_revenue DESC
    """
    df_gold_customer = spark.sql(sql_customer)
    df_gold_customer.createOrReplaceTempView("gold_revenue_by_customer")
    df_gold_customer.write.mode("overwrite").parquet(os.path.join(gold_dir, "gold_revenue_by_customer"))
    
    # 4. Build Gold Customer Segmentation
    sql_segmentation = """
        WITH customer_summary AS (
            SELECT 
                c.customer_id,
                COALESCE(COUNT(o.order_id), 0) AS order_count,
                COALESCE(SUM(o.total_amount), 0.0) AS total_spent
            FROM silver_customers c
            LEFT JOIN silver_orders o ON c.customer_id = o.customer_id AND o.is_valid = TRUE
            WHERE c.is_valid = TRUE
            GROUP BY c.customer_id
        ),
        segmented AS (
            SELECT 
                customer_id,
                order_count,
                total_spent,
                CASE 
                    WHEN total_spent >= 1000.0 THEN 'High-Value'
                    WHEN order_count > 1 THEN 'Repeat'
                    WHEN order_count = 1 THEN 'One-Time'
                    ELSE 'Inactive'
                END AS segment_type
            FROM customer_summary
        )
        SELECT 
            segment_type,
            COUNT(customer_id) AS customer_count,
            ROUND(AVG(total_spent), 2) AS avg_revenue,
            ROUND(SUM(total_spent), 2) AS total_revenue
        FROM segmented
        GROUP BY segment_type
        ORDER BY total_revenue DESC
    """
    df_gold_segmentation = spark.sql(sql_segmentation)
    df_gold_segmentation.createOrReplaceTempView("gold_customer_segmentation")
    df_gold_segmentation.write.mode("overwrite").parquet(os.path.join(gold_dir, "gold_customer_segmentation"))
    
    print("\n--- GOLD AGGREGATION PREVIEWS ---")
    print("\nTop 5 Products by Revenue:")
    df_gold_product.show(5)
    
    print("\nCustomer Segmentation Breakdown:")
    df_gold_segmentation.show()
    print("=========================================\n")
    
    return df_gold_product, df_gold_customer, df_gold_segmentation

def get_spark_session(app_name="Gold_Pipeline_Orchestrator"):
    active = SparkSession.getActiveSession()
    if active:
        return active
    if "SPARK_REMOTE" in os.environ and not os.environ["SPARK_REMOTE"].startswith("sc://"):
        os.environ.pop("SPARK_REMOTE", None)
    builder = SparkSession.builder.appName(app_name)
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()

if __name__ == "__main__":
    spark = get_spark_session("Gold_Pipeline_Orchestrator")
    
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
    data_dir = os.path.join(root_dir, "data")
    wh_dir = os.path.join(data_dir, "warehouse")
    
    run_gold_pipeline(spark, data_dir, wh_dir)
