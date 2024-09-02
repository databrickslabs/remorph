--Query type: DQL
WITH temp_result AS (
    SELECT 'file1' AS name, 1000 AS size
    UNION ALL
    SELECT 'file2', 2000
)
SELECT name, CAST(size AS FLOAT) / 128.0 - CAST(FILEPROPERTY(name, 'SpaceUsed') AS INT) / 128.0 AS AvailableSpaceInMB
FROM temp_result