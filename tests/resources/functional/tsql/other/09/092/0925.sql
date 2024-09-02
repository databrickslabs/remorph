--Query type: DDL
WITH customerCTE AS (
    SELECT custkey, name, nationkey
    FROM (
        VALUES (1, 'Customer1', 1),
               (2, 'Customer2', 2)
    ) AS customer(custkey, name, nationkey)
),
ordersCTE AS (
    SELECT custkey, orderdate, totalprice
    FROM (
        VALUES (1, 1, '1995-01-01', 1000.0),
               (2, 1, '1995-01-02', 2000.0)
    ) AS orders(orderkey, custkey, orderdate, totalprice)
)
SELECT c.custkey, c.name, SUM(o.totalprice) AS total_order_value
FROM customerCTE c
JOIN ordersCTE o ON c.custkey = o.custkey
WHERE c.nationkey = 1 AND o.orderdate >= '1995-01-01'
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 100000
ORDER BY total_order_value DESC;

SELECT * FROM customer;

SELECT * FROM orders;