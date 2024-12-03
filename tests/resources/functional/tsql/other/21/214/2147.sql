--Query type: DCL
WITH temp_result AS (SELECT 1 AS id, 'test' AS name)
SELECT 1 AS id, 'test' AS name
FROM temp_result
WHERE EXISTS (SELECT 1 FROM temp_result);
