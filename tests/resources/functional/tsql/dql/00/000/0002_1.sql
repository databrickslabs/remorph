-- tsql sql:
WITH temp_result AS (SELECT '012,345.67' AS str_value UNION ALL SELECT '12,345.67' UNION ALL SELECT ' 12,345.67') SELECT CONVERT(DECIMAL(18,2), REPLACE(REPLACE(str_value, ',', ''), ' ', '')) AS num_value FROM temp_result
