-- tsql sql:
WITH temp_result AS (
    SELECT SCHEMA_NAME(schema_id) AS SchemaName
    FROM sys.objects
)
SELECT SchemaName
FROM temp_result
ORDER BY SchemaName ASC
