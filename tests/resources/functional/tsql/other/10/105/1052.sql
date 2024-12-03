--Query type: DDL
WITH orders AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey, 'O' AS o_orderstatus, 100.00 AS o_totalprice, '2020-01-01' AS o_orderdate
    UNION ALL
    SELECT 2, 2, 'O', 200.00, '2020-01-02'
    UNION ALL
    SELECT 3, 3, 'O', 300.00, '2020-01-03'
),
    mv_orders AS (
    SELECT MAX(o_orderdate) AS max_o_orderdate, MIN(o_totalprice) AS min_o_totalprice, o.o_orderkey, o.o_custkey, o.o_orderstatus
    FROM orders o
    GROUP BY o.o_orderkey, o.o_custkey, o.o_orderstatus
)
SELECT * FROM mv_orders;
