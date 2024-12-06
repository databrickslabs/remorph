--
-- Verify a simple CTE.
--

-- snowflake sql:
WITH a AS (SELECT 1, 2, 3)
SELECT * FROM a;

-- databricks sql:
WITH a AS (SELECT 1, 2, 3)
SELECT * FROM a;
