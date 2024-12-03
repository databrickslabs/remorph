--Query type: DQL
WITH temp_result AS (
    SELECT o.object_id, s.schema_id, s.name AS schema_name, o.name AS object_name
    FROM sys.objects o
    INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
)
SELECT QUOTENAME(DB_NAME()) + N'.' + QUOTENAME(schema_name) + N'.' + QUOTENAME(object_name), *
FROM temp_result;
