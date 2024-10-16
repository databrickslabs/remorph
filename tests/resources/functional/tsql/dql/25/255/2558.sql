--Query type: DQL
SELECT DB_ID([value]) AS [Database ID]
FROM (
    VALUES (N'customer')
) AS temp_result([value]);