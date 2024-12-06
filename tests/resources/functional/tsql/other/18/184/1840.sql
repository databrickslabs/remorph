-- tsql sql:
DECLARE @myvar CHAR(20);
SET @myvar = 'This is a test';

WITH T1 AS (
    SELECT @myvar AS value
),
T2 AS (
    SELECT 'constant' AS name
)

SELECT TOP 1 T1.value, T2.name
FROM T1
CROSS JOIN T2
