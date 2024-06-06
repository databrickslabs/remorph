## MAX with DISTINCT

The MAX function is identical in Databricks SQL and T-SQL. As DISTINCT is merely removing duplicates,
its presence or otherwise is irrelevant to the MAX function.

-- tsql sql:
SELECT MAX(DISTINCT col1) FROM t1;

-- databricks sql:
SELECT MAX(DISTINCT col1) FROM t1;
