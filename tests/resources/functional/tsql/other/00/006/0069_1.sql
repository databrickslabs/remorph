-- tsql sql:
WITH customer_orders AS (
    SELECT c_custkey, '***' AS c_name, o_orderkey, CONVERT(VARCHAR(10), o_orderdate, 120) AS o_orderdate
    FROM #customer_orders
)
SELECT *
FROM customer_orders;
