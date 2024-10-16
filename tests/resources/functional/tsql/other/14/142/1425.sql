--Query type: DCL
WITH temp_result AS (SELECT column1, column2 FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS temp_result(column1, column2))
SELECT TOP 1 *
FROM temp_result
ORDER BY NEWID();