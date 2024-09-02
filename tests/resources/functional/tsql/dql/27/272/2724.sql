--Query type: DQL
WITH my_indexes AS (
    SELECT 1 AS index_id, 'index1' AS index_name, DB_NAME(database_id) AS database_name, OBJECT_SCHEMA_NAME(object_id, database_id) AS schema_name, OBJECT_NAME(object_id, database_id) AS object_name
    FROM sys.dm_db_index_operational_stats(null, null, null, null)
)
SELECT QUOTENAME(mi.database_name) + N'.' + QUOTENAME(mi.schema_name) + N'.' + QUOTENAME(mi.object_name), *
FROM my_indexes mi;