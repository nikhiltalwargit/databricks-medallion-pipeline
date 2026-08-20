# Databricks Lakehouse BI Dashboard Guide

## Dashboard Overview
This guide provides step-by-step instructions for creating the **E-Commerce Executive Sales & Quality Dashboard** in Databricks SQL using queries from `src/dashboard/dashboard_queries.sql`.

---

## Dashboard Visual Layout

```
+-----------------------------------------------------------------------------------+
|                            E-COMMERCE EXECUTIVE DASHBOARD                         |
+-------------------------------------------------+---------------------------------+
| Tile 1: Top 10 Products by Revenue (Bar Chart)  | Tile 3: Customer Segmentation   |
| X-Axis: product_name | Y-Axis: total_revenue    | Chart Type: Donut / Pie Chart   |
+-------------------------------------------------+---------------------------------+
| Tile 2: Customer Revenue Tiers (Histogram)      | Tile 4: Weekly Revenue Trend    |
| X-Axis: revenue_tier | Y-Axis: customer_count   | Chart Type: Line Chart          |
+-------------------------------------------------+---------------------------------+
```

---

## Step-by-Step Setup Instructions

1. **Open Databricks SQL:** Navigate to **Dashboards** -> **Create Dashboard** in your Databricks workspace.
2. **Title:** Name your dashboard `E-Commerce Sales & Medallion Pipeline Analytics`.
3. **Add Tiles:**
   - **Tile 1 (Top 10 Products):** Create a new Query widget using Tile 1 query from `dashboard_queries.sql`. Set chart type to **Bar Chart**, X-Axis = `product_name`, Y-Axis = `total_revenue`.
   - **Tile 2 (Revenue Distribution):** Add Query widget using Tile 2 query. Set chart type to **Column Chart**, X-Axis = `revenue_tier`, Y-Axis = `customer_count`.
   - **Tile 3 (Segmentation Pie):** Add Query widget using Tile 3 query. Set chart type to **Pie Chart**, Key = `segment_type`, Value = `customer_count`.
   - **Tile 4 (Weekly Trend Line):** Add Query widget using Tile 4 query. Set chart type to **Line Chart**, X-Axis = `week_start_date`, Y-Axis = `total_revenue`.
4. **Publish & Share:** Save dashboard and configure auto-refresh (e.g. daily at 06:00 UTC).
