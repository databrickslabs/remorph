--Query type: DQL
SELECT CAST(1 AS INT) ^ CAST(2 AS INT) AS xor_result FROM (VALUES (1, 2)) AS temp_result(a_int_value, b_int_value);