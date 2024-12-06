-- tsql sql:
WITH last_change AS (
    SELECT MAX(last_user_update) AS last_change_commit_time
    FROM sys.dm_db_index_usage_stats
    WHERE database_id = DB_ID()
        AND object_id = OBJECT_ID('customer')
)
SELECT *
FROM last_change;
