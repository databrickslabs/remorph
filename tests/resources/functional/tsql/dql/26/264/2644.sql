-- tsql sql:
WITH temp_result AS (SELECT 'a' AS col1, 1 AS col2, 'b' AS col3, NULL AS col4) SELECT JSON_ARRAY(col1, col2, col3, col4) FROM temp_result
