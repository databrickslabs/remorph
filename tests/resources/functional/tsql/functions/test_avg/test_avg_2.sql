-- AVG with DISTINCT clause
--
-- This function is directly equivalent in Databricks.

-- tsql sql:
SELECT AVG(DISTINCT col1) AS vagcol1 FROM tabl;

-- databricks sql:
SELECT AVG(DISTINCT col1) AS vagcol1 FROM tabl;
