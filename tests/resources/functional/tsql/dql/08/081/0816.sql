-- tsql sql:
WITH temp_result AS ( SELECT 1 AS c_custkey, 100.0 AS c_acctbal UNION ALL SELECT 2, 200.0 UNION ALL SELECT 3, 300.0 ) SELECT * FROM temp_result ORDER BY c_acctbal DESC
