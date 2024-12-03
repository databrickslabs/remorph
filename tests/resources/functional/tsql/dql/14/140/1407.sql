--Query type: DQL
WITH MaterializedViewOverhead AS (
    SELECT 'MaterializedView1' AS ViewName, 1000 AS [RowCount], 10.0 AS StorageSizeMB
    UNION ALL
    SELECT 'MaterializedView2', 500, 5.0
)
SELECT *
FROM MaterializedViewOverhead;
