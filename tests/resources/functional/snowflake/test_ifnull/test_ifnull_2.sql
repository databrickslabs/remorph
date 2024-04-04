
-- snowflake sql:
SELECT ifnull(col1) AS ifnull_col1 FROM tabl;

-- databricks sql:
SELECT COALESCE(col1) AS ifnull_col1 FROM tabl;
