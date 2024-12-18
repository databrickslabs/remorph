-- tsql sql:
WITH temp_result AS (SELECT column1 FROM (VALUES (1), (2)) AS temp (column1))
SELECT column1 AS [File Name]
FROM temp_result;
