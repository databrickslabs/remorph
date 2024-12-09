-- ## ... UNION ALL ...
--
-- Verify simple UNION ALL handling.
--
-- snowflake sql:

SELECT 1
UNION ALL
SELECT 2;

-- databricks sql:
(SELECT 1)
UNION ALL
(SELECT 2);
