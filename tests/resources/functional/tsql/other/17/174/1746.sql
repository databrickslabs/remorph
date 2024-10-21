--Query type: DCL
DECLARE @d datetime;
SELECT @d = DATEADD(day, 1, '2022-01-01');
WITH dates AS (
    SELECT 0 AS day
    UNION ALL
    SELECT day + 1
    FROM dates
    WHERE day < 6
)
SELECT @d + day AS date
FROM dates
OPTION (MAXRECURSION 0);