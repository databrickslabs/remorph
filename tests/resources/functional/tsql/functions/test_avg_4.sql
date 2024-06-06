-- AVG with the DISTINCT and OVER clauses
--
-- This function is not directly equivalent in Databricks, when used with the DISTINCT clause,
-- as Databricks SQL, like a number of SQL implementations, does not support the use of DISTINCT
-- in the AVG function.
--
-- The behavior is reproduced using a subquery to generate the DISTINCT version of the column

-- tsql sql:
SELECT AVG(DISTINCT col1) OVER (PARTITION BY col1 ORDER BY col1 ASC) AS avgcol1 FROM tabl;

-- databricks sql:
SELECT AVG(distinctCol1.col1) OVER (PARTITION BY col1 ORDER BY col1 ASC) AS avgcol1
FROM (
         SELECT DISTINCT col1
         FROM tabl
     ) AS distinctCol1;
