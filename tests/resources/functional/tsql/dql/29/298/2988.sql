--Query type: DQL
SELECT ~ CAST(a_int_value AS INT), ~ CAST(b_int_value AS INT) FROM (VALUES (1, 2), (3, 4), (5, 6)) AS temp_result_set (a_int_value, b_int_value);