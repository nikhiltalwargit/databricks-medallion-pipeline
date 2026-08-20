-- Gold Layer Transformation 3: Daily & Weekly Revenue Trends
-- Summarizes sales performance over daily and weekly windows for trend analysis

SELECT 
    DATE_TRUNC('week', order_date) AS week_start_date,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM silver_orders
WHERE is_valid = TRUE
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week_start_date ASC;
