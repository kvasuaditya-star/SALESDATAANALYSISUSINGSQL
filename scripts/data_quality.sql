-- SQL script for Data Quality Assurance & Database Integrity Audit

-- 1. Check for duplicate customer emails
SELECT email, COUNT(*) as occurrence_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- 2. Check for duplicate customer names (potential duplicate accounts)
SELECT first_name, last_name, COUNT(*) as occurrence_count
FROM customers
GROUP BY first_name, last_name
HAVING COUNT(*) > 1;

-- 3. Check for orphan orders (orders without a valid customer_id)
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 4. Check for orphan order items (referencing non-existent orders or products)
SELECT oi.order_item_id, oi.order_id, oi.product_id
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.order_id IS NULL OR p.product_id IS NULL;

-- 5. Validate pricing integrity: Check if unit_price in order_items matches product price
SELECT oi.order_id, oi.product_id, oi.unit_price as transactional_price, p.price as current_product_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE ABS(oi.unit_price - p.price) > 0.001;

-- 6. Check for order amount discrepancy (sum of items vs total_amount in orders table)
WITH computed_totals AS (
    SELECT order_id, SUM(quantity * unit_price) as computed_total
    FROM order_items
    GROUP BY order_id
)
SELECT o.order_id, o.total_amount as logged_total, ct.computed_total, 
       ABS(o.total_amount - ct.computed_total) as difference
FROM orders o
JOIN computed_totals ct ON o.order_id = ct.order_id
WHERE ABS(o.total_amount - ct.computed_total) > 0.01;

-- 7. Check for temporal logic anomalies (orders placed before customer joined)
SELECT o.order_id, o.customer_id, o.order_date, c.join_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date < c.join_date;

-- 8. Check for temporal logic anomalies (payments made before order date)
SELECT p.payment_id, p.order_id, p.payment_date, o.order_date
FROM payments p
JOIN orders o ON p.order_id = o.order_id
WHERE p.payment_date < o.order_date;

-- 9. Check for duplicate payments for the same order (if multiple, list them)
SELECT order_id, COUNT(*) as payment_count, SUM(payment_amount) as total_paid
FROM payments
GROUP BY order_id
HAVING COUNT(*) > 1;
