--Query type: DDL
WITH temp_result AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, '123-456-7890' AS c_phone, 'USA' AS n_name, '123 Main St' AS c_address, 'This is a comment' AS c_comment, 10.00 AS l_extendedprice, 0.10 AS l_discount
    UNION ALL
    SELECT 2 AS c_custkey, 'Customer2' AS c_name, 200.00 AS c_acctbal, '987-654-3210' AS c_phone, 'Canada' AS n_name, '456 Elm St' AS c_address, 'This is another comment' AS c_comment, 20.00 AS l_extendedprice, 0.20 AS l_discount
),

    temp_result2 AS (
    SELECT c_custkey, c_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone, c_comment
    FROM temp_result
    GROUP BY c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
)

SELECT c_custkey, c_name, revenue, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_result2
WHERE c_acctbal > 0.00
ORDER BY revenue DESC;