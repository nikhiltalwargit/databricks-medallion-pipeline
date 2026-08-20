# Medallion Architecture Specification

## Input Schemas
- `customers.csv`: `customer_id` (INT), `customer_name` (STRING), `email` (STRING), `country` (STRING), `signup_date` (DATE), `customer_segment` (STRING), `lifetime_value` (DECIMAL(10,2)).
- `orders.csv`: `order_id` (INT), `customer_id` (INT), `order_date` (DATE), `product_id` (INT), `quantity` (INT), `unit_price` (DECIMAL(10,2)), `total_amount` (DECIMAL(10,2)), `order_status` (STRING), `payment_date` (DATE).
- `products.csv`: `product_id` (INT), `product_name` (STRING), `category` (STRING), `price` (DECIMAL(10,2)), `cost` (DECIMAL(10,2)), `stock_quantity` (INT), `reorder_level` (INT).

## Medallion Layer Rules
- **Bronze:** Delta tables `bronze_customers`, `bronze_orders`, `bronze_products`. Schema enforcement + metadata.
- **Silver:** Delta tables `silver_customers`, `silver_orders`, `silver_products`. Append `is_valid` boolean & `quality_check_result` JSON struct.
- **Gold:** Delta tables:
  1. `gold_sales_by_product`
  2. `gold_revenue_by_customer`
  3. `gold_daily_weekly_trends`
  4. `gold_customer_segmentation`
- **Dashboard:** 4 Databricks SQL visualization queries.
