
-- snowflake sql:
SELECT last_value(col1) over (partition by col1 order by col2) AS last_value_col1 FROM tabl;

-- databricks sql:
SELECT LAST_VALUE(col1) OVER (PARTITION BY col1 ORDER BY col2 NULLS LAST) AS last_value_col1 FROM tabl;
