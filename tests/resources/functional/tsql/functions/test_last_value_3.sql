-- ## LAST_VALUE over PARTITIONS
--
-- The LAST_VALUE function is identical in TSql and Databricks.

-- tsql sql:
SELECT col1, col2, col3, LAST_VALUE(col1) OVER (PARTITION BY col2 ORDER BY col2 DESC) AS last_value FROM tabl;

-- databricks sql:
SELECT col1, col2, col3, LAST_VALUE(col1) OVER (PARTITION BY col2 ORDER BY col2 DESC) AS last_value FROM tabl;
