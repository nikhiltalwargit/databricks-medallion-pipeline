import sys
import os
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src/silver"))

import importlib

validate_completeness = importlib.import_module("01_quality_completeness").validate_completeness
validate_uniqueness = importlib.import_module("02_quality_uniqueness").validate_uniqueness

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.appName("PyTest_Silver").master("local[1]").getOrCreate()

def test_validate_completeness_flagging(spark):
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("email", StringType(), True)
    ])
    data = [(1, "user@test.com"), (2, ""), (3, None)]
    df = spark.createDataFrame(data, schema)
    
    result_df = validate_completeness(df, ["id", "email"])
    rows = result_df.collect()
    
    assert rows[0]["completeness_status"] == "PASS"
    assert "FAIL" in rows[1]["completeness_status"]
    assert "FAIL" in rows[2]["completeness_status"]

def test_validate_uniqueness_flagging(spark):
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    data = [(101, "Alice"), (101, "Alice"), (102, "Bob")]
    df = spark.createDataFrame(data, schema)
    
    result_df = validate_uniqueness(df, ["id"])
    rows = result_df.collect()
    
    statuses = [r["uniqueness_status"] for r in rows]
    assert "PASS" in statuses
    assert "FAIL: Duplicate PK [id]" in statuses
