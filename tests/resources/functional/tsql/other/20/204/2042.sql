--Query type: DCL
DROP USER AbolrousHazem;
WITH TempResult AS (
    SELECT *
    FROM (
        VALUES (1, 'John Doe'),
               (2, 'Jane Doe')
    ) AS TempResult(id, name)
)
SELECT *
FROM TempResult