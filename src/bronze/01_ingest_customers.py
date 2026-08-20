#!/usr/bin/env python3
"""
Bronze Layer — Ingest Raw Customers CSV into Delta Table
"""

import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DecimalType
from pyspark.sql import functions as F

def get_spark_session(app_name="Bronze_Ingest_Customers"):
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

CUSTOMER_SCHEMA = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("country", StringType(), True),
    StructField("signup_date", DateType(), True),
    StructField("customer_segment", StringType(), True),
    StructField("lifetime_value", DecimalType(10, 2), True),
])

def ingest_customers(spark, csv_path, output_path=None, table_name="bronze_customers"):
    print(f"Reading raw customers from {csv_path}...")
    df_raw = spark.read.csv(
        csv_path,
        header=True,
        schema=CUSTOMER_SCHEMA,
        dateFormat="yyyy-MM-dd"
    )
    
    # Enrich with audit metadata
    df_bronze = df_raw.withColumn("_ingested_at", F.current_timestamp()) \
                      .withColumn("_source_file", F.lit(os.path.basename(csv_path)))
    
    record_count = df_bronze.count()
    print(f"Ingested {record_count} records into Bronze Customers.")
    
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        (df_bronze.write
         .format("delta" if "delta" in spark.conf.get("spark.sql.extensions", "") else "parquet")
         .mode("overwrite")
         .save(os.path.join(output_path, "bronze_customers")))
        
    df_bronze.createOrReplaceTempView(table_name)
    return df_bronze

if __name__ == "__main__":
    spark = get_spark_session()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, "../../data/customers.csv")
    out_dir = os.path.join(base_dir, "../../data/warehouse")
    ingest_customers(spark, data_file, out_dir)
