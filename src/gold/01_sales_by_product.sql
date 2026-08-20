-- Gold Layer Transformation 1: Sales by Product Aggregation
-- Selects only valid orders and valid products (is_valid = True)

SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM silver_orders o
JOIN silver_products p ON o.product_id = p.product_id
WHERE o.is_valid = TRUE 
  AND p.is_valid = TRUE
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;
