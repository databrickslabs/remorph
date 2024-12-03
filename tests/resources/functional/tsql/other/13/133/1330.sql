--Query type: DDL
CREATE TABLE orders (order_key INT, totalprice DECIMAL(10, 2), orderdate DATE);
INSERT INTO orders (order_key, totalprice, orderdate)
SELECT order_key, totalprice, orderdate
FROM (VALUES (1, 100.00, '1995-01-01'), (2, 200.00, '1996-01-01')) AS orders(order_key, totalprice, orderdate);
SELECT * FROM orders WHERE orderdate > '1995-01-01';
-- REMORPH CLEANUP: DROP TABLE orders;
