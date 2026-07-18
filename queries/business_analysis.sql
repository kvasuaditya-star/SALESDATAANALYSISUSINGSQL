-- SQL Queries for Sales Data Analysis & Business Intelligence

-- 1. Monthly Revenue Trends
-- Calculates total revenue generated per month (excluding Cancelled orders)
SELECT 
    strftime('%Y-%m', o.order_date) as sales_month,
    COUNT(o.order_id) as total_orders,
    ROUND(SUM(o.total_amount), 2) as total_revenue
FROM orders o
WHERE o.status != 'Cancelled'
GROUP BY sales_month
ORDER BY sales_month ASC;

-- 2. Top-Selling Products by Quantity
-- Identifies the most popular products by quantity sold
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) as total_quantity_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'Cancelled'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- 3. Top-Selling Products by Revenue
-- Identifies which products generate the most revenue
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) as total_quantity_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'Cancelled'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Profit Margins by Product Category
-- Computes the profit margin for each product category (Revenue - Product Cost)
SELECT 
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) as total_revenue,
    ROUND(SUM(oi.quantity * p.cost), 2) as total_cost,
    ROUND(SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * p.cost), 2) as total_profit,
    ROUND(((SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * p.cost)) / SUM(oi.quantity * oi.unit_price)) * 100, 2) as profit_margin_percent
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'Cancelled'
GROUP BY p.category
ORDER BY total_profit DESC;
