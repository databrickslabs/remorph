-- tsql sql:
CREATE TABLE #t1 (col1 INT, col2 INT);

WITH src AS (
  SELECT a, b, c
  FROM (
    VALUES (1, 2, 11),
           (3, 4, 12),
           (5, 6, 7)
  ) AS src (a, b, c)
)
INSERT INTO #t1 (col1, col2)
SELECT a, b
FROM src
WHERE c > 10;

SELECT * FROM #t1;
-- REMORPH CLEANUP: DROP TABLE #t1;
