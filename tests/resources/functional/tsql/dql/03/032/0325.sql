-- tsql sql:
WITH temp_result AS (SELECT name, object_id, type_desc FROM (VALUES ('table1', 1, 'USER_TABLE'), ('table2', 2, 'VIEW')) AS tables (name, object_id, type_desc))
SELECT name, object_id, type_desc
FROM temp_result
WHERE OBJECTPROPERTY(object_id, N'SchemaId') = SCHEMA_ID(N'public')
ORDER BY type_desc, name;
