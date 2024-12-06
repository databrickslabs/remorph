-- ## ... UNION ...
--
-- Verify simple UNION handling.
--
-- snowflake sql:

SELECT 1
UNION
SELECT 2;

-- databricks sql:
(SELECT 1)
UNION
(SELECT 2);
