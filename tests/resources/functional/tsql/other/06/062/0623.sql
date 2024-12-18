-- tsql sql:
DROP TABLE IF EXISTS TempResult;

WITH TempResult AS (
    SELECT *
    FROM (
        VALUES (1, 'John'),
               (2, 'Alice')
    ) AS T(id, name)
)

SELECT *
FROM TempResult
WHERE id = 1
