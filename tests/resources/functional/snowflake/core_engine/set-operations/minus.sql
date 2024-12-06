-- ## ... MINUS ...
--
-- Verify simple MINUS handling: it is an alias for EXCEPT.
--
-- snowflake sql:

SELECT 1
MINUS
SELECT 2;

-- databricks sql:
(SELECT 1)
EXCEPT
(SELECT 2);
