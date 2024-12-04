--
-- CTEs are visible to all the SELECT queries within a subsequent sequence of set operations.
--

-- snowflake sql:
WITH a AS (SELECT 1, 2, 3)

SELECT 4, 5, 6
UNION
SELECT * FROM a;

-- databricks sql:
WITH a AS (SELECT 1, 2, 3)

(SELECT 4, 5, 6)
UNION
(SELECT * FROM a);
