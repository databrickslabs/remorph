-- tsql sql:
DROP TABLE IF EXISTS #test_ignore_nulls;
CREATE TABLE #test_ignore_nulls
(
    column_a INT,
    column_b INT
);
INSERT INTO #test_ignore_nulls (column_a, column_b)
VALUES
    (1, 10),
    (2, 20),
    (3, 30),
    (4, 40),
    (5, 50);
WITH cte AS
(
    SELECT column_a,
           column_b,
           LAG(column_a, 1, 0) OVER (ORDER BY column_a) AS prev_column_a,
           LEAD(column_b, 1, 0) OVER (ORDER BY column_a) AS next_column_b
    FROM #test_ignore_nulls
)
SELECT column_a,
       column_b,
       prev_column_a,
       next_column_b,
       IIF(column_a > prev_column_a, 'increased', 'decreased') AS trend
FROM cte
ORDER BY column_a;
