#!/usr/bin/env python3
"""
Bronze Layer — Ingest Raw Products CSV into Delta Table
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType
from pyspark.sql import functions as F

def get_spark_session(app_name="Bronze_Ingest_Products"):
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
