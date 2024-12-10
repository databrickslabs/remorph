-- tsql sql:
CREATE TABLE orders (orderkey INT, totalprice DECIMAL(10, 2), orderdate DATE);
INSERT INTO orders (orderkey, totalprice, orderdate)
VALUES (1, 10.0, '2020-01-01'), (2, 20.0, '2020-01-02');
WITH secured_orders AS (
    SELECT orderkey, totalprice, orderdate
    FROM orders
    WHERE totalprice > 0 AND orderdate >= '2020-01-01'
)
SELECT *
FROM secured_orders;
-- REMORPH CLEANUP: DROP TABLE orders;
