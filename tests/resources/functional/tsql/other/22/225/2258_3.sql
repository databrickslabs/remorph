--Query type: TCL
WITH temp_customer AS (
    SELECT c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment
    FROM #temp_customer
),
    temp_orders AS (
    SELECT o_orderkey, o_custkey
    FROM #temp_orders
),
    temp_lineitem AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM #temp_lineitem
),
    temp_nation AS (
    SELECT n_nationkey, n_name
    FROM #temp_nation
)
SELECT 
    c.c_custkey,
    c.c_name,
    SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue,
    c.c_acctbal,
    n.n_name,
    c.c_address,
    c.c_phone,
    c.c_comment
FROM temp_customer c
INNER JOIN temp_orders o ON c.c_custkey = o.o_custkey
INNER JOIN temp_lineitem l ON o.o_orderkey = l.l_orderkey
INNER JOIN temp_nation n ON c.c_custkey = n.n_nationkey
WHERE c.c_acctbal > 0.00
AND l.l_orderkey IN (
    SELECT l_orderkey
    FROM temp_lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY c.c_custkey, c.c_name, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
ORDER BY revenue DESC;