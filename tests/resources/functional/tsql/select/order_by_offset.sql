--
-- ORDER BY can have an optional OFFSET clause.
--

-- tsql sql:
SELECT *
FROM a_table
ORDER BY 1
OFFSET 1 ROW;

-- databricks sql:
SELECT *
FROM a_table
ORDER BY 1
OFFSET 1;
