--Query type: DQL
DECLARE @d smalldatetime = '2009-09-11 12:42:12';
WITH cte AS (
    SELECT 'Input' AS col1, @d AS col2
)
SELECT col1, col2 FROM cte
UNION ALL
SELECT 'Truncated to minute' AS col1, DATETRUNC(minute, @d) AS col2
UNION ALL
SELECT 'Truncated to second' AS col1, DATETRUNC(second, @d) AS col2
