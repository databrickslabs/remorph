--Query type: DQL
WITH query_stats AS (
    SELECT 1 AS dbid, 1 AS objectid, 'SELECT * FROM customer' AS text
    UNION ALL
    SELECT 2 AS dbid, 2 AS objectid, 'SELECT * FROM orders' AS text
)
SELECT DB_NAME(qs.dbid) AS database_name,
       OBJECT_SCHEMA_NAME(qs.objectid, qs.dbid) AS schema_name,
       OBJECT_NAME(qs.objectid, qs.dbid) AS object_name,
       qs.text AS query_statement
FROM query_stats qs
CROSS APPLY (VALUES (qs.text)) AS ca(text)
WHERE qs.objectid IS NOT NULL;