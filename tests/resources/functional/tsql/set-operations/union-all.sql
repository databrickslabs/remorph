-- ## ... UNION ALL ...
--
-- Verify simple UNION ALL handling.
--
-- tsql sql:

SELECT 1
UNION ALL
SELECT 2;

-- databricks sql:
(SELECT 1)
UNION ALL
(SELECT 2);
