-- tsql sql:
WITH orders AS (
    SELECT 1 AS o_orderkey, '2022-01-01' AS o_orderdate, 100.00 AS o_totalprice
    UNION ALL
    SELECT 2 AS o_orderkey, '2022-01-02' AS o_orderdate, 200.00 AS o_totalprice
    UNION ALL
    SELECT 3 AS o_orderkey, '2022-01-03' AS o_orderdate, 300.00 AS o_totalprice
)
SELECT *
FROM orders;
