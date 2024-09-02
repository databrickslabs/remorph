--Query type: DQL
WITH temp_result AS ( SELECT object_id FROM ( VALUES (1), (2), (3) ) AS objects(object_id) ) SELECT DISTINCT OBJECT_SCHEMA_NAME(object_id) FROM temp_result