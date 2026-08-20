#!/usr/bin/env python3
"""
Bronze Layer — Ingest Raw Orders CSV into Delta Table
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DecimalType
from pyspark.sql import functions as F

def get_spark_session(app_name="Bronze_Ingest_Orders"):
    active = SparkSession.getActiveSession()
    if active:
        return active
    if "SPARK_REMOTE" in os.environ and not os.environ["SPARK_REMOTE"].startswith("sc://"):
        os.environ.pop("SPARK_REMOTE", None)
    builder = SparkSession.builder.appName(app_name)
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()

ORDER_SCHEMA = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DecimalType(10, 2), True),
    StructField("total_amount", DecimalType(10, 2), True),
    StructField("order_status", StringType(), True),
    StructField("payment_date", DateType(), True),
])

def ingest_orders(spark, csv_path, output_path=None, table_name="bronze_orders"):
    print(f"Reading raw orders from {csv_path}...")
    df_raw = spark.read.csv(
        csv_path,
        header=True,
        schema=ORDER_SCHEMA,
        dateFormat="yyyy-MM-dd"
    )
    
    # Enrich with audit metadata
    df_bronze = df_raw.withColumn("_ingested_at", F.current_timestamp()) \
                      .withColumn("_source_file", F.lit(os.path.basename(csv_path)))
    
    record_count = df_bronze.count()
    print(f"Ingested {record_count} records into Bronze Orders.")
    
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        (df_bronze.write
         .format("parquet")
         .mode("overwrite")
         .save(os.path.join(output_path, "bronze_orders")))
        
    df_bronze.createOrReplaceTempView(table_name)
    return df_bronze

if __name__ == "__main__":
    spark = get_spark_session()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../../data/orders.csv")
    out_dir = os.path.join(base_dir, "../../data/warehouse")
    ingest_orders(spark, data_file, out_dir)
