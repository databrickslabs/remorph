--Query type: DQL
WITH temp_result AS ( SELECT 1 AS c_custkey, 'John' AS c_name UNION ALL SELECT 2, 'Jane' ) SELECT * FROM temp_result ORDER BY c_custkey;