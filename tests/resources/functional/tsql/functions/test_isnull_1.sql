-- ## ISNULL
--
-- In TSQL ISNULL is a function that returns the first expression if it is not NULL,
-- otherwise it returns the second expression.
--
-- In Databricks ISNULL is a function that returns boolean true if the single argument is NULL,
-- so it is replaced with IFNULL, which is the equivalent function in Databricks.
--
-- tsql sql:
SELECT ISNULL(col1, 0) AS pcol1 FROM table;

-- databricks sql:
SELECT IFNULL(col1, 0) AS pcol1 FROM table;
