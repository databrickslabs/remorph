-- tsql sql:
SELECT DB_ID([value]) AS [Database ID]
FROM (
    VALUES (N'customer')
) AS temp_result([value]);
