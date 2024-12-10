-- tsql sql:
WITH temp_result AS (
    SELECT c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
    FROM (
        VALUES (1, 'Customer1', 100.00, 'Nation1', 'Address1', 'Phone1', 'Comment1'),
               (2, 'Customer2', 200.00, 'Nation2', 'Address2', 'Phone2', 'Comment2')
    ) AS temp_table (c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment)
),
     temp_orders AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.00),
               (2, 2, 200.00)
    ) AS temp_table (o_orderkey, o_custkey, o_totalprice)
),
     temp_lineitem AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES (1, 100.00, 0.10),
               (2, 200.00, 0.20)
    ) AS temp_table (l_orderkey, l_extendedprice, l_discount)
)
SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_result
    JOIN temp_orders ON c_custkey = o_custkey
    JOIN temp_lineitem ON o_orderkey = l_orderkey
WHERE c_acctbal > 0.00
      AND l_orderkey IN (
        SELECT l_orderkey
        FROM temp_lineitem
        GROUP BY l_orderkey
        HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
    )
GROUP BY c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
ORDER BY revenue DESC;
