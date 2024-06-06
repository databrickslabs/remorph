## STDEV

The STDEV function is identical in Databricks SQL and T-SQL.


-- tsql sql:
SELECT STDEV(DISTINCT col1) FROM t1;

-- databricks sql:
SELECT STDEV(DISTINCT col1) FROM t1;
