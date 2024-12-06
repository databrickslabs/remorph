-- tsql sql:
WITH temp_result AS (
    SELECT '1' AS c1, '2' AS c2, '3' AS c3
    UNION ALL
    SELECT '4', '5', '6'
)
SELECT *
FROM temp_result;
