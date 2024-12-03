--Query type: DQL
WITH temp_result AS (
    SELECT 'schema' AS schema_name, 'source_clone' AS object_name, 1 AS is_ddl
)
SELECT *
FROM temp_result;
EXEC sp_helptext 'schema.source_clone';
