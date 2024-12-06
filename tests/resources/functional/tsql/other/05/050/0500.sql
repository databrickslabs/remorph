-- tsql sql:
WITH T1 AS (
    SELECT 1001 AS suppkey, 'Supplier#000000001' AS s_name, 1000.00 AS total_revenue
    UNION ALL
    SELECT 1002 AS suppkey, 'Supplier#000000002' AS s_name, 2000.00 AS total_revenue
),
T2 AS (
    SELECT 1 AS l_orderkey, 1001 AS l_suppkey, 100.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2 AS l_orderkey, 1002 AS l_suppkey, 200.00 AS l_extendedprice, 0.2 AS l_discount
),
T3 AS (
    SELECT 1 AS n_nationkey, 'Nation1' AS n_name
    UNION ALL
    SELECT 2 AS n_nationkey, 'Nation2' AS n_name
),
temp_lineitem AS (
    SELECT 1 AS l_orderkey, 1001 AS l_suppkey, 100.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2 AS l_orderkey, 1002 AS l_suppkey, 200.00 AS l_extendedprice, 0.2 AS l_discount
)
SELECT
    T1.suppkey,
    T1.s_name,
    SUM(T2.l_extendedprice * (1 - T2.l_discount)) AS revenue,
    T1.total_revenue,
    T3.n_name,
    'Address1' AS s_address,
    'Phone1' AS s_phone,
    'Comment1' AS s_comment
FROM T1
JOIN T2 ON T1.suppkey = T2.l_suppkey
JOIN T3 ON T1.suppkey = T3.n_nationkey  -- Assuming suppkey matches n_nationkey for simplicity
WHERE T1.total_revenue > 0.00
AND T2.l_orderkey IN (
    SELECT l_orderkey
    FROM temp_lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY T1.suppkey, T1.s_name, T1.total_revenue, T3.n_name
ORDER BY revenue DESC;
