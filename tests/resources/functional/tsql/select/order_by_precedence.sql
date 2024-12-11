--
-- ORDER BY appears at the end of a sequence of set operations, and applies to the result of the set operation.
--
-- tsql sql:

SELECT 1 AS n
UNION
SELECT 2

ORDER BY n DESC; -- Applies to the complete UNION, not just the final expression.

-- databricks sql:
(SELECT 1 AS n)
 UNION
(SELECT 2)

ORDER BY n DESC;
