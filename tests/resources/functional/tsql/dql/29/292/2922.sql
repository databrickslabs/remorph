-- tsql sql:
SELECT name, object_id, type_desc FROM (VALUES (OBJECT_NAME(274100017), 274100017, 'USER_TABLE')) AS temp_result (name, object_id, type_desc) WHERE name = OBJECT_NAME(274100017);
