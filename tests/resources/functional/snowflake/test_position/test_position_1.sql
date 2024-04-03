
-- source:
SELECT position('exc', col1) AS position_col1 FROM tabl;

-- databricks_sql:
SELECT LOCATE('exc', col1) AS position_col1 FROM tabl;
