-- tsql sql:
DBCC FLUSHAUTHCACHE;
SELECT 'Authorization cache flushed' AS result
FROM (
    VALUES (
        1
    )
) AS temp_table (column_name);
