-- ## AVG with the DISTINCT and OVER clauses
--
-- This function is directly equivalent in Databricks when used with the DISTINCT clause,

-- tsql sql:
SELECT AVG(DISTINCT col1) OVER (PARTITION BY col1 ORDER BY col1 ASC) AS avgcol1 FROM tabl;

-- databricks sql:
SELECT AVG(DISTINCT col1) OVER (PARTITION BY col1 ORDER BY col1 ASC) AS avgcol1 FROM tabl;
