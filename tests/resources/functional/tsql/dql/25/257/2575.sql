--Query type: DQL
WITH temp_result AS ( SELECT object_id FROM ( VALUES (1), (2), (3) ) AS t(object_id) ) SELECT DISTINCT OBJECT_SCHEMA_NAME(object_id, 1) AS schema_name FROM temp_result