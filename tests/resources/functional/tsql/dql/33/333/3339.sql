--Query type: DQL
SELECT DISTINCT OBJECT_SCHEMA_NAME(t.table_id, 1) AS schema_name
FROM (
    VALUES (1), (2), (3)
) AS t(table_id);