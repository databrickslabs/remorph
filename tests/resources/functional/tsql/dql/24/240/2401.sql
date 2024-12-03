--Query type: DQL
WITH temp_result AS (
    SELECT (
        SELECT COUNT(*)
        FROM sys.dm_db_index_usage_stats
        WHERE user_seeks > 0 OR user_scans > 0 OR user_lookups > 0
    ) AS Reads,
    (
        SELECT COUNT(*)
        FROM sys.dm_db_index_usage_stats
        WHERE user_updates > 0
    ) AS Writes
)
SELECT Reads, Writes, GETDATE() AS 'As of'
FROM temp_result
