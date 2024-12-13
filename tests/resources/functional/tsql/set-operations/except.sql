-- ## ... EXCEPT ...
--
-- Verify simple EXCEPT handling.
--
-- tsql sql:

SELECT 1
EXCEPT
SELECT 2;

-- databricks sql:
(SELECT 1)
EXCEPT
(SELECT 2);
