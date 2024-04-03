
-- source:
SELECT JSON_EXTRACT_PATH_TEXT('{}', path_col) FROM demo1;

-- databricks_sql:
SELECT GET_JSON_OBJECT('{}', CONCAT('$.', path_col)) FROM demo1;
