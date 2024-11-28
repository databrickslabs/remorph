-- ## ... INTERSECT ...
--
-- Verify simple INTERSECT handling.
--
-- tsql sql:

SELECT 1
INTERSECT
SELECT 2;

-- databricks sql:
(SELECT 1)
INTERSECT
(SELECT 2);
