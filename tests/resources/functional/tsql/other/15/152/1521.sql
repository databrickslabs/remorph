-- tsql sql:
DECLARE @customer_id INT;
SET @customer_id = 123;

WITH orders AS (
    SELECT 1 AS order_id, 123 AS customer_id, '2022-01-01' AS order_date, 100.00 AS total, 'Shipped' AS status
    UNION ALL
    SELECT 2 AS order_id, 123 AS customer_id, '2022-01-15' AS order_date, 200.00 AS total, 'Delivered' AS status
    UNION ALL
    SELECT 3 AS order_id, 456 AS customer_id, '2022-02-01' AS order_date, 50.00 AS total, 'Pending' AS status
)

SELECT *
FROM orders
WHERE customer_id = @customer_id;
