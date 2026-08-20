-- Gold Layer Transformation 2: Revenue by Customer Aggregation
-- Selects only valid orders and customers (is_valid = True)

SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(SUM(o.total_amount), 2) AS lifetime_value_actual
FROM silver_customers c
JOIN silver_orders o ON c.customer_id = o.customer_id
WHERE c.is_valid = TRUE 
  AND o.is_valid = TRUE
GROUP BY c.customer_id, c.customer_name, c.customer_segment
ORDER BY total_revenue DESC;
