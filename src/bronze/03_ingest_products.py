#!/usr/bin/env python3
"""
Bronze Layer — Ingest Raw Products CSV into Delta Table
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType
from pyspark.sql import functions as F

def get_spark_session(app_name="Bronze_Ingest_Products"):
    active = SparkSession.getActiveSession()
    if active:
        return active
    if "SPARK_REMOTE" in os.environ and not os.environ["SPARK_REMOTE"].startswith("sc://"):
        os.environ.pop("SPARK_REMOTE", None)
    builder = SparkSession.builder.appName(app_name)
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        builder = builder.master("local[*]")
    return builder.getOrCreate()

PRODUCT_SCHEMA = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("price", DecimalType(10, 2), True),
    StructField("cost", DecimalType(10, 2), True),
    StructField("stock_quantity", IntegerType(), True),
    StructField("reorder_level", IntegerType(), True),
])

def ingest_products(spark, csv_path, output_path=None, table_name="bronze_products"):
    print(f"Reading raw products from {csv_path}...")
    df_raw = spark.read.csv(
        csv_path,
        header=True,
        schema=PRODUCT_SCHEMA
    )
    
    # Enrich with audit metadata
    df_bronze = df_raw.withColumn("_ingested_at", F.current_timestamp()) \
                      .withColumn("_source_file", F.lit(os.path.basename(csv_path)))
    
    record_count = df_bronze.count()
    print(f"Ingested {record_count} records into Bronze Products.")
    
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        (df_bronze.write
         .format("parquet")
         .mode("overwrite")
         .save(os.path.join(output_path, "bronze_products")))
        
    df_bronze.createOrReplaceTempView(table_name)
    return df_bronze

if __name__ == "__main__":
    spark = get_spark_session()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../../data/products.csv")
    out_dir = os.path.join(base_dir, "../../data/warehouse")
    ingest_products(spark, data_file, out_dir)
