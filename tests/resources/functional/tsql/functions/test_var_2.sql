-- ## VAR with DISTINCT
--
-- The VAR funciton is identical in TSQL and Databricks. Using DISTINCT with VAR
-- will not change the results as variance is calculated on unique values already.

-- tsql sql:
SELECT VAR(DISTINCT col1) AS sum_col1 FROM tabl;

-- databricks sql:
SELECT VAR(DISTINCT col1) AS sum_col1 FROM tabl;
