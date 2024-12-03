--Query type: DML
INSERT INTO orders (order_key, cust_key, order_status)
SELECT order_key, cust_key, order_status
FROM (
    VALUES (1, 2, 'PENDING'),
           (3, 4, 'SHIPPED')
) AS orders (order_key, cust_key, order_status);
