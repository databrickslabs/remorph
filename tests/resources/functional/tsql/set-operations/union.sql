-- ## ... UNION ...
--
-- Verify simple UNION handling.
--
-- tsql sql:

SELECT 1
UNION
SELECT 2;

-- databricks sql:
(SELECT 1)
UNION
(SELECT 2);
