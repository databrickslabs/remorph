-- ## GROUPING_ID
--
-- GROUPING_ID is directly equivalent in Databricks SQL and TSQL.

-- tsql sql:
SELECT GROUPING_ID(col1, col2) FROM t1 GROUP BY CUBE(col1, col2);

-- databricks sql:
SELECT GROUPING_ID(col1, col2) FROM t1 GROUP BY CUBE(col1, col2);
