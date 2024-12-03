--Query type: DCL
DECLARE @orderDate DATE = '1995-01-01';
WITH orders AS (
    SELECT 1 AS o_orderkey, '1995-01-01' AS o_orderdate
    UNION ALL
    SELECT 2, '1995-01-02'
)
SELECT *
FROM orders
WHERE o_orderdate > @orderDate
