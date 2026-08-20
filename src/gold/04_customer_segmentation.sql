-- Gold Layer Transformation 4: Customer Segmentation Cohort Analysis
-- Cohort rules:
-- High-Value: Total Revenue >= $1,000
-- Repeat: Orders > 1 AND Total Revenue < $1,000
-- One-Time: Orders = 1
-- Inactive: Orders = 0

WITH customer_summary AS (
    SELECT 
        c.customer_id,
        COALESCE(COUNT(o.order_id), 0) AS order_count,
        COALESCE(SUM(o.total_amount), 0.0) AS total_spent
    FROM silver_customers c
    LEFT JOIN silver_orders o ON c.customer_id = o.customer_id AND o.is_valid = TRUE
    WHERE c.is_valid = TRUE
    GROUP BY c.customer_id
),
segmented AS (
    SELECT 
        customer_id,
        order_count,
        total_spent,
        CASE 
            WHEN total_spent >= 1000.0 THEN 'High-Value'
            WHEN order_count > 1 THEN 'Repeat'
            WHEN order_count = 1 THEN 'One-Time'
            ELSE 'Inactive'
        END AS segment_type
    FROM customer_summary
)
SELECT 
    segment_type,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(total_spent), 2) AS avg_revenue,
    ROUND(SUM(total_spent), 2) AS total_revenue
FROM segmented
GROUP BY segment_type
ORDER BY total_revenue DESC;
