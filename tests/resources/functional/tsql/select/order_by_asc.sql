--
-- Explicit (redundant) ascending ORDER BY on the end of a SELECT.
--
-- tsql sql:

SELECT 1 AS n
ORDER BY n ASC;

-- databricks sql:
SELECT 1 AS n
ORDER BY n;
