--Query type: DQL
WITH temp_result AS (SELECT 'function_name' AS func_name, 'schema_name' AS schema_name)
SELECT OBJECT_ID(func_name) AS object_id, OBJECTPROPERTY(OBJECT_ID(func_name), 'IsDeterministic') AS is_deterministic
FROM (VALUES ('function_name', 'schema_name')) AS temp_result(func_name, schema_name)