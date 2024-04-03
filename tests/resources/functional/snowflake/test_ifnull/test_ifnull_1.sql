
-- source:
SELECT ifnull(col1, 'NA') AS ifnull_col1 FROM tabl;

-- databricks_sql:
SELECT COALESCE(col1, 'NA') AS ifnull_col1 FROM tabl;
