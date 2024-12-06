-- tsql sql:
SELECT ISJSON(json_value) AS is_json FROM (VALUES ('true')) AS temp_table(json_value);
