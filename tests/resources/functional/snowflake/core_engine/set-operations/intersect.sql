-- ## ... INTERSECT ...
--
-- Verify simple INTERSECT handling.
--
-- snowflake sql:

SELECT 1
INTERSECT
SELECT 2;

-- databricks sql:
(SELECT 1)
INTERSECT
(SELECT 2);
