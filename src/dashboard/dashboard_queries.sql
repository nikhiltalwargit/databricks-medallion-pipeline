-- Databricks SQL Dashboard Visualization Queries

-- Tile 1: Top 10 Products by Total Revenue (Bar Chart)
-- Visualization Type: Bar Chart | X-Axis: product_name | Y-Axis: total_revenue
SELECT 
    product_name,
    category,
    total_orders,
    total_revenue,
    avg_order_value
FROM gold_sales_by_product
ORDER BY total_revenue DESC
LIMIT 10;

-- Tile 2: Customer Revenue Distribution (Histogram / Box Plot)
-- Visualization Type: Histogram | X-Axis: total_revenue (Buckets) | Y-Axis: Count of Customers
SELECT 
    CASE 
        WHEN total_revenue < 100 THEN '$0 - $100'
        WHEN total_revenue BETWEEN 100 AND 500 THEN '$100 - $500'
        WHEN total_revenue BETWEEN 500 AND 1000 THEN '$500 - $1,000'
        WHEN total_revenue BETWEEN 1000 AND 2500 THEN '$1,000 - $2,500'
        ELSE '$2,500+'
    END AS revenue_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(SUM(total_revenue), 2) AS tier_total_revenue
FROM gold_revenue_by_customer
GROUP BY 
    CASE 
        WHEN total_revenue < 100 THEN '$0 - $100'
        WHEN total_revenue BETWEEN 100 AND 500 THEN '$100 - $500'
        WHEN total_revenue BETWEEN 500 AND 1000 THEN '$500 - $1,000'
        WHEN total_revenue BETWEEN 1000 AND 2500 THEN '$1,000 - $2,500'
        ELSE '$2,500+'
    END
ORDER BY MIN(total_revenue) ASC;

-- Tile 3: Customer Segmentation Share (Donut / Pie Chart)
-- Visualization Type: Pie Chart | Slice: segment_type | Value: customer_count
SELECT 
    segment_type,
    customer_count,
    avg_revenue,
    total_revenue
FROM gold_customer_segmentation;

-- Tile 4: Weekly Revenue Trend (Line Chart)
-- Visualization Type: Line Chart | X-Axis: week_start_date | Y-Axis: total_revenue
SELECT 
    DATE_TRUNC('week', order_date) AS week_start_date,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM silver_orders
WHERE is_valid = TRUE
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week_start_date ASC;
