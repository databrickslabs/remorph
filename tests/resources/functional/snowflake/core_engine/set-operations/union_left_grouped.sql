-- ## (SELECT …) UNION SELECT …
--
-- Verify UNION handling when the LHS of the union is explicitly wrapped in parentheses.
--
-- snowflake sql:

(SELECT a, b from c) UNION SELECT x, y from z;

-- databricks sql:
(SELECT a, b FROM c) UNION (SELECT x, y  FROM z);
