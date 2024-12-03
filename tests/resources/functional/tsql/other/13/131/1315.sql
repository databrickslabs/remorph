--Query type: DDL
CREATE TABLE orders ( id INTEGER PRIMARY KEY, order_date DATE ) AS EDGE;
WITH order_items AS (
    SELECT 1 AS id, '2020-01-01' AS order_date
    UNION ALL
    SELECT 2 AS id, '2020-01-15' AS order_date
    UNION ALL
    SELECT 3 AS id, '2020-02-01' AS order_date
)
SELECT * FROM order_items;
