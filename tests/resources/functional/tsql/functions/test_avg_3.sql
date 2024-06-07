-- ## AVG with ALL clause
--
-- This function is directly equivalent in Databricks.
-- However, as ALL does not change the result, it is not necessary to include it in the Databricks SQL and
-- it is elided.

-- tsql sql:
SELECT AVG(ALL col1) AS vagcol1 FROM tabl;

-- databricks sql:
SELECT AVG(col1) AS vagcol1 FROM tabl;
