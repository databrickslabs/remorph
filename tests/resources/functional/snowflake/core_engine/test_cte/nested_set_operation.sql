--
-- Verify a CTE that includes set operations.
--

-- snowflake sql:
WITH a AS (
    SELECT 1, 2, 3
    UNION
    SELECT 4, 5, 6
)
SELECT * FROM a;

-- databricks sql:
WITH a AS (
    (SELECT 1, 2, 3)
    UNION
    (SELECT 4, 5, 6)
)
SELECT * FROM a;
