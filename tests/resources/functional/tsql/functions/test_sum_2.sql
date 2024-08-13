-- ## SUM with DISTINCT
--
-- The SUM function is identical in TSQL and Databricks

-- tsql sql:
SELECT sum(DISTINCT col1) AS sum_col1 FROM tabl;

-- databricks sql:
SELECT SUM(DISTINCT col1) AS sum_col1 FROM tabl;
