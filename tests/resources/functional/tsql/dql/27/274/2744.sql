--Query type: DQL
WITH temp_result AS ( SELECT 1 AS id ) SELECT SCHEMA_NAME(id) FROM temp_result
