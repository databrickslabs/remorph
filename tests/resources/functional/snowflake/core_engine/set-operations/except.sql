-- ## ... EXCEPT ...
--
-- Verify simple EXCEPT handling.
--
-- snowflake sql:

SELECT 1
EXCEPT
SELECT 2;

-- databricks sql:
(SELECT 1)
EXCEPT
(SELECT 2);
