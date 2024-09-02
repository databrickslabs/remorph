--Query type: DDL
WITH temp_result AS (
    SELECT 1 AS custkey, 'Customer1' AS name, 100.00 AS acctbal, 'USA' AS nation, '123 Main St' AS address, '123-456-7890' AS phone, 'This is a comment' AS comment
    UNION ALL
    SELECT 2 AS custkey, 'Customer2' AS name, 200.00 AS acctbal, 'Canada' AS nation, '456 Elm St' AS address, '987-654-3210' AS phone, 'This is another comment' AS comment
),
     temp_orders AS (
    SELECT 1 AS orderkey, 1 AS custkey, 100.00 AS totalprice
    UNION ALL
    SELECT 2 AS orderkey, 1 AS custkey, 200.00 AS totalprice
    UNION ALL
    SELECT 3 AS orderkey, 2 AS custkey, 50.00 AS totalprice
),
     temp_lineitem AS (
    SELECT 1 AS orderkey, 10.00 AS extendedprice, 0.10 AS discount
    UNION ALL
    SELECT 2 AS orderkey, 20.00 AS extendedprice, 0.20 AS discount
    UNION ALL
    SELECT 3 AS orderkey, 5.00 AS extendedprice, 0.05 AS discount
)
SELECT tr.custkey, tr.name, SUM(tl.extendedprice * (1 - tl.discount)) AS revenue, tr.acctbal, tr.nation, tr.address, tr.phone, tr.comment
FROM temp_result tr
JOIN temp_orders tos ON tr.custkey = tos.custkey
JOIN temp_lineitem tl ON tos.orderkey = tl.orderkey
WHERE tr.acctbal > 0.00
GROUP BY tr.custkey, tr.name, tr.acctbal, tr.nation, tr.address, tr.phone, tr.comment
ORDER BY revenue DESC