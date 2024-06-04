## VARP with DISTINCT

The VARP funciton is identical in TSQL and Databricks. Using DISTINCT with VARP
will not change the results as variance is calculated on unique values already.

-- tsql sql:
SELECT VARP(DISTINCT col1) AS sum_col1 FROM tabl;

-- databricks sql:
SELECT VARP(DISTINCT col1) AS sum_col1 FROM tabl;
