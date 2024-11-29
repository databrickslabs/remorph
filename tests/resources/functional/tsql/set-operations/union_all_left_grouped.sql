-- ## (SELECT …) UNION ALL SELECT …
--
-- Verify UNION handling when the LHS of the union is explicitly wrapped in parentheses.
--
-- tsql sql:

(SELECT a, b from c) UNION ALL SELECT x, y from z;

-- databricks sql:
(SELECT a, b FROM c) UNION ALL (SELECT x, y  FROM z);
