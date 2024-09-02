--Query type: DCL
DROP SERVER AUDIT SPECIFICATION HIPAA_Audit_Specification;

WITH temp_result AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 1000.00 AS c_acctbal, 'Nation1' AS n_name, 'Address1' AS c_address, 'Phone1' AS c_phone, 'Comment1' AS c_comment
    UNION ALL
    SELECT 2 AS c_custkey, 'Customer2' AS c_name, 2000.00 AS c_acctbal, 'Nation2' AS n_name, 'Address2' AS c_address, 'Phone2' AS c_phone, 'Comment2' AS c_comment
),

    temp_orders AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey
    UNION ALL
    SELECT 2 AS o_orderkey, 2 AS o_custkey
),

    temp_lineitem AS (
    SELECT 1 AS l_orderkey, 100.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2 AS l_orderkey, 200.00 AS l_extendedprice, 0.2 AS l_discount
)

SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_result
JOIN temp_orders ON c_custkey = o_custkey
JOIN temp_lineitem ON o_orderkey = l_orderkey
WHERE c_acctbal > 0.00 AND l_orderkey IN (
    SELECT l_orderkey
    FROM temp_lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
ORDER BY revenue DESC