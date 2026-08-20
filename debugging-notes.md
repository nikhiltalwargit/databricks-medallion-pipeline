# Debugging & Error Resolution Log

## Incident 1: Schema Inconsistency on Raw Date Ingestion
- **Symptom:** `signup_date` and `order_date` parsed as `NULL` during Bronze CSV read.
- **Root Cause:** Default Spark CSV reader expected `MM/dd/yyyy` format, whereas `generate_sample_data.py` output ISO standard `yyyy-MM-dd`.
- **Resolution:** Explicitly specified `dateFormat="yyyy-MM-dd"` in `spark.read.csv()` options across `01_ingest_customers.py` and `02_ingest_orders.py`.

## Incident 2: PySpark Window Function Order Column Requirement
- **Symptom:** `AnalysisException: Window frame requires an orderby clause` during Silver uniqueness check execution.
- **Root Cause:** PySpark `Window.partitionBy("customer_id")` requires an explicit ordering specification when evaluating `row_number()`.
- **Resolution:** Added conditional ordering column `orderBy(F.col("_ingested_at"))` in `02_quality_uniqueness.py`.

## Incident 3: Left Anti Join Column Alias Shadowing
- **Symptom:** `AnalysisException: Reference 'customer_id' is ambiguous` during referential integrity check.
- **Root Cause:** Both Orders and Customers DataFrames contained `customer_id` columns with identical names.
- **Resolution:** Explicitly aliased DataFrames (`o` for Orders, `c` for Customers) and selected `o.*` post-join in `04_quality_referential_integrity.py`.

## Incident 4: Python Module Numeric Import Syntax Error
- **Symptom:** `SyntaxError: invalid decimal literal` when executing `create_silver_tables.py` and `ingest_all.py`.
- **Root Cause:** Python parser treats module names starting with numbers (e.g. `01_ingest_customers.py`) as numeric literals in standard `from 01_... import ...` statements.
- **Resolution:** Leveraged `importlib.import_module("01_ingest_customers")` to dynamically import numeric-prefixed modules, preserving exact required repository file naming conventions while ensuring 100% valid Python syntax.

## Incident 5: Spark Connect / Databricks Master Configuration Conflict
- **Symptom:** `PySparkRuntimeError: [CANNOT_CONFIGURE_SPARK_CONNECT_MASTER] Spark Connect server and Spark master cannot be configured together` when executing PySpark scripts in Databricks.
- **Root Cause:** Hardcoding `.master("local[*]")` on `SparkSession.builder` conflicted with Databricks pre-configured Spark Connect socket / active Spark session.
- **Resolution:** Refactored `get_spark_session()` across all PySpark modules to check `SparkSession.getActiveSession()` first, and dynamically omit `.master("local[*]")` when running inside Databricks (`"DATABRICKS_RUNTIME_VERSION" in os.environ`).

## Incident 6: Databricks Subshell SPARK_REMOTE Invalid Connect URL Error
- **Symptom:** `PySparkValueError: [INVALID_CONNECT_URL] Invalid URL for Spark Connect: The URL must start with 'sc://'` when executing `!python` subshell commands in Databricks.
- **Root Cause:** Databricks 14+ subshell magic populates `SPARK_REMOTE="unix:///databricks/sparkconnect/grpc.sock..."`. PySpark Connect client attempts to parse this unix socket URL as a standard `sc://` connection.
- **Resolution:** Sanitized `get_spark_session()` across all PySpark scripts: if `SPARK_REMOTE` is present in `os.environ` and does not start with `sc://`, it is popped (`os.environ.pop("SPARK_REMOTE", None)`), enabling clean fallback to the cluster JVM Spark context.

## Incident 7: Databricks Runtime 14+ DatabricksSession Requirement
- **Symptom:** `RuntimeError: Only remote Spark sessions using Databricks Connect are supported. Use DatabricksSession.builder to create a remote Spark session instead`.
- **Root Cause:** Databricks Runtime 14.3 LTS Shared / Serverless clusters require `databricks.connect.DatabricksSession` for remote session building.
- **Resolution:** Enhanced `get_spark_session()` across all PySpark modules to attempt `DatabricksSession.builder.appName(app_name).getOrCreate()` when `databricks.connect` is present, ensuring 100% smooth execution on Databricks 14+ clusters.
