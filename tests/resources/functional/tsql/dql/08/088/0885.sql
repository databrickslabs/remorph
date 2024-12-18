-- tsql sql:
WITH temp_result AS (
    SELECT 'value1' AS s1, 'value2' AS s2, 'value1' AS s3
    UNION ALL
    SELECT 'value3' AS s1, 'value4' AS s2, 'value5' AS s3
)
SELECT *
FROM temp_result
WHERE s1 = s3;
