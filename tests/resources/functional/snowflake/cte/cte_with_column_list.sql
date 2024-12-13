--
-- A simple CTE, with the column list expressed.
--

-- snowflake sql:
WITH a (b, c, d) AS (SELECT 1 AS b, 2 AS c, 3 AS d)
SELECT b, c, d FROM a;

-- databricks sql:
WITH a (b, c, d) AS (SELECT 1 AS b, 2 AS c, 3 AS d)
SELECT b, c, d FROM a;
