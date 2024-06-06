## CUME_DIST

The CUME_DIST function is identical in TSql and Databricks.

-- tsql sql:
SELECT col1, col2, cume_dist() OVER (PARTITION BY col1 ORDER BY col2) AS cume_dist FROM tabl;

-- databricks sql:
SELECT col1, col2, cume_dist() OVER (PARTITION BY col1 ORDER BY col2) AS cume_dist FROM tabl;
