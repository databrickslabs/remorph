-- ## SUM
--
-- The SUM function is identical in TSQL and Databricks

-- tsql sql:
SELECT sum(col1) AS sum_col1 FROM tabl;

-- databricks sql:
SELECT SUM(col1) AS sum_col1 FROM tabl;
