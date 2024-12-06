-- tsql sql:
WITH temp_result AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 1000.00 AS c_acctbal, 'Nation1' AS n_name, 'Address1' AS c_address, 'Phone1' AS c_phone, 'Comment1' AS c_comment
    UNION ALL
    SELECT 2, 'Customer2', 2000.00, 'Nation2', 'Address2', 'Phone2', 'Comment2'
),
    temp_orders AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey
    UNION ALL
    SELECT 2, 2
),
    temp_lineitem AS (
    SELECT 1 AS l_orderkey, 100000.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2, 200000.00, 0.2
)
SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_result
JOIN temp_orders ON temp_result.c_custkey = temp_orders.o_custkey
JOIN temp_lineitem ON temp_orders.o_orderkey = temp_lineitem.l_orderkey
WHERE temp_result.c_acctbal > 0.00 AND temp_lineitem.l_orderkey IN (
    SELECT l_orderkey FROM temp_lineitem GROUP BY l_orderkey HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY temp_result.c_custkey, temp_result.c_name, temp_result.c_acctbal, temp_result.n_name, temp_result.c_address, temp_result.c_phone, temp_result.c_comment
ORDER BY revenue DESC;
