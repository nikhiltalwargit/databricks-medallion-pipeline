import sys
import os
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType, BooleanType

from decimal import Decimal

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.appName("PyTest_Gold").master("local[1]").getOrCreate()

def test_gold_sales_by_product_math(spark):
    orders_schema = StructType([
        StructField("order_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("total_amount", DecimalType(10, 2), True),
        StructField("is_valid", BooleanType(), True)
    ])
    products_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("is_valid", BooleanType(), True)
    ])
    
    orders_data = [
        (1, 10, Decimal("100.00"), True),
        (2, 10, Decimal("200.00"), True),
        (3, 10, Decimal("50.00"), False), # Should be excluded
    ]
    products_data = [(10, "Widget A", "Gadgets", True)]
    
    df_orders = spark.createDataFrame(orders_data, orders_schema)
    df_products = spark.createDataFrame(products_data, products_schema)
    
    df_orders.createOrReplaceTempView("silver_orders")
    df_products.createOrReplaceTempView("silver_products")
    
    sql = """
        SELECT 
            p.product_id,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_revenue
        FROM silver_orders o
        JOIN silver_products p ON o.product_id = p.product_id
        WHERE o.is_valid = TRUE AND p.is_valid = TRUE
        GROUP BY p.product_id
    """
    res = spark.sql(sql).collect()[0]
    assert res["total_orders"] == 2
    assert float(res["total_revenue"]) == 300.00
