
-- snowflake sql:
SELECT first_value(col1) AS first_value_col1 FROM tabl;

-- databricks sql:
SELECT FIRST_VALUE(col1) AS first_value_col1 FROM tabl;
