-- tsql sql:
WITH temp_result AS (SELECT 1 AS col1, 2 AS col2)
SELECT col1 AS [Index Column 1], col2 AS [Index Column 2]
FROM temp_result;
