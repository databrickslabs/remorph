
-- snowflake sql:
SELECT JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key[1]') FROM demo1;

-- databricks sql:
SELECT GET_JSON_OBJECT(json_data, '$.level_1_key.level_2_key[1]') FROM demo1;
