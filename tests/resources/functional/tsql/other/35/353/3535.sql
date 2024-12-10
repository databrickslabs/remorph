-- tsql sql:
WITH temp_result AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name, 100.00 AS c_acctbal, 'Nation1' AS n_name, 'Address1' AS c_address, 'Phone1' AS c_phone, 'Comment1' AS c_comment
    UNION ALL
    SELECT 2, 'Customer2', 200.00, 'Nation2', 'Address2', 'Phone2', 'Comment2'
)
SELECT c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
FROM temp_result
WHERE c_acctbal > 0.00
ORDER BY c_acctbal DESC;
