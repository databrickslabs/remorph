-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/lead-transact-sql?view=sql-server-ver16

DROP TABLE IF EXISTS #test_ignore_nulls;
CREATE TABLE #test_ignore_nulls (column_a int, column_b int);
GO

INSERT INTO #test_ignore_nulls VALUES
    (1, 8),
    (2, 9),
    (3, NULL),
    (4, 10),
    (5, NULL),
    (6, NULL),
    (7, 11);

SELECT column_a, column_b,
      [Previous value for column_b] = LAG(column_b) RESPECT NULLS OVER (ORDER BY column_a),
      [Next value for column_b] = LEAD(column_b) RESPECT NULLS OVER (ORDER BY column_a)
FROM #test_ignore_nulls
ORDER BY column_a;

--Identical output
SELECT column_a, column_b,
      [Previous value for column_b] = LAG(column_b)  OVER (ORDER BY column_a),
      [Next value for column_b] = LEAD(column_b)  OVER (ORDER BY column_a)
FROM #test_ignore_nulls
ORDER BY column_a;

--cleanup
DROP TABLE #test_ignore_nulls;