# Data Model & Schema Specification

## Source & Medallion Entity Relationship Diagram

```
+--------------------+           +--------------------+           +--------------------+
|     CUSTOMERS      |           |       ORDERS       |           |      PRODUCTS      |
+--------------------+           +--------------------+           +--------------------+
| customer_id (PK)   |<----------| customer_id (FK)   |           | product_id (PK)    |
| customer_name      |           | order_id (PK)      |---------->| product_name       |
| email              |           | order_date         |           | category           |
| country            |           | product_id (FK)    |           | price              |
| signup_date        |           | quantity           |           | cost               |
| customer_segment   |           | unit_price         |           | stock_quantity     |
| lifetime_value     |           | total_amount       |           | reorder_level      |
+--------------------+           | order_status       |           +--------------------+
                                 | payment_date       |
                                 +--------------------+
```

---

## 1. Table Specifications — Bronze Layer

### `bronze_customers`
| Column Name | Data Type | Nullable | Source Field | Metadata / Description |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | INT | Yes | `customer_id` | Raw customer identifier |
| `customer_name` | STRING | Yes | `customer_name` | Full customer name |
| `email` | STRING | Yes | `email` | Email address |
| `country` | STRING | Yes | `country` | Country code / name |
| `signup_date` | DATE | Yes | `signup_date` | Signup date |
| `customer_segment` | STRING | Yes | `customer_segment` | Basic / Standard / Premium |
| `lifetime_value` | DECIMAL(10,2) | Yes | `lifetime_value` | Estimated LTV |
| `_ingested_at` | TIMESTAMP | No | System | Audit timestamp |
| `_source_file` | STRING | No | System | Input CSV path |

### `bronze_orders`
| Column Name | Data Type | Nullable | Source Field | Metadata / Description |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | INT | Yes | `order_id` | Primary key |
| `customer_id` | INT | Yes | `customer_id` | Foreign key → customers |
| `order_date` | DATE | Yes | `order_date` | Order placement date |
| `product_id` | INT | Yes | `product_id` | Foreign key → products |
| `quantity` | INT | Yes | `quantity` | Quantity ordered |
| `unit_price` | DECIMAL(10,2) | Yes | `unit_price` | Unit price |
| `total_amount` | DECIMAL(10,2) | Yes | `total_amount` | Order total amount |
| `order_status` | STRING | Yes | `order_status` | Pending / Completed / Cancelled |
| `payment_date` | DATE | Yes | `payment_date` | Payment fulfillment date |
| `_ingested_at` | TIMESTAMP | No | System | Audit timestamp |
| `_source_file` | STRING | No | System | Input CSV path |

### `bronze_products`
| Column Name | Data Type | Nullable | Source Field | Metadata / Description |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | INT | Yes | `product_id` | Primary key |
| `product_name` | STRING | Yes | `product_name` | Product title |
| `category` | STRING | Yes | `category` | Category classification |
| `price` | DECIMAL(10,2) | Yes | `price` | Retail price |
| `cost` | DECIMAL(10,2) | Yes | `cost` | Wholesale cost |
| `stock_quantity` | INT | Yes | `stock_quantity` | Inventory count |
| `reorder_level` | INT | Yes | `reorder_level` | Minimum stock threshold |
| `_ingested_at` | TIMESTAMP | No | System | Audit timestamp |
| `_source_file` | STRING | No | System | Input CSV path |

---

## 2. Table Specifications — Silver Layer

All Silver tables contain the complete Bronze schemas plus two mandatory quality governance columns:
- `is_valid` (BOOLEAN): `True` if record passed all completeness, uniqueness, referential integrity, and type validation checks.
- `quality_check_result` (STRING/JSON): Details specific checks failed (e.g. `{"completeness": "FAIL: NULL email", "uniqueness": "PASS"}`).

---

## 3. Table Specifications — Gold Layer

### `gold_sales_by_product`
- `product_id` (INT)
- `product_name` (STRING)
- `category` (STRING)
- `total_orders` (BIGINT)
- `total_revenue` (DECIMAL(12,2))
- `avg_order_value` (DECIMAL(10,2))

### `gold_revenue_by_customer`
- `customer_id` (INT)
- `customer_name` (STRING)
- `customer_segment` (STRING)
- `total_orders` (BIGINT)
- `total_revenue` (DECIMAL(12,2))
- `avg_order_value` (DECIMAL(10,2))
- `lifetime_value_actual` (DECIMAL(12,2))

### `gold_daily_weekly_trends`
- `time_period` (STRING - Date or Week Start Date)
- `period_type` (STRING - 'DAILY' / 'WEEKLY')
- `total_orders` (BIGINT)
- `total_revenue` (DECIMAL(12,2))
- `avg_order_value` (DECIMAL(10,2))

### `gold_customer_segmentation`
- `segment_type` (STRING - 'High-Value' / 'Repeat' / 'One-Time' / 'Inactive')
- `customer_count` (BIGINT)
- `avg_revenue` (DECIMAL(12,2))
- `total_revenue` (DECIMAL(12,2))
