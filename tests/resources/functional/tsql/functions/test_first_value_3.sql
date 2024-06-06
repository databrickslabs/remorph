-- ## FIRST_VALUE over PARTITIONS
--
-- The FIRST_VALUE function is identical in TSql and Databricks.

-- tsql sql:
SELECT col1, col2, col3, FIRST_VALUE(col1) OVER (PARTITION BY col2 ORDER BY col2 DESC) AS first_value FROM tabl;

-- databricks sql:
SELECT col1, col2, col3, FIRST_VALUE(col1) OVER (PARTITION BY col2 ORDER BY col2 DESC) AS first_value FROM tabl;
