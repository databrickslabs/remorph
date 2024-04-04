
-- snowflake sql:
SELECT JSON_EXTRACT_PATH_TEXT(json_data, path_col) FROM demo1;

-- databricks sql:
SELECT GET_JSON_OBJECT(json_data, CONCAT('$.', path_col)) FROM demo1;
