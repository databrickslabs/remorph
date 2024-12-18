-- tsql sql:
WITH TempResult AS (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS FirstUse
    FROM (
        VALUES (1), (1)
    ) AS t(c)
),
TempResult2 AS (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS SecondUse
    FROM (
        VALUES (1), (1)
    ) AS t(c)
)
SELECT FirstUse, SecondUse
FROM TempResult
CROSS JOIN TempResult2
