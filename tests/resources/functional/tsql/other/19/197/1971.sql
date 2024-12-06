-- tsql sql:
DROP TABLE #TempResult;

WITH TempResult AS (
    SELECT *
    FROM (
        VALUES (1, 'John'),
               (2, 'Alice')
    ) AS TempResult(id, name)
)

SELECT *
FROM TempResult;
