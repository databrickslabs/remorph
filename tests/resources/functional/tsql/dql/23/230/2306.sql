-- tsql sql:
WITH temp_result AS (SELECT -45.01 AS value UNION SELECT -181.01 UNION SELECT 0 UNION SELECT 0.1472738 UNION SELECT 197.1099392) SELECT 'The ATAN of ' + CONVERT(varchar, value) + ' is: ' + CONVERT(varchar, ATAN(value)) FROM temp_result
