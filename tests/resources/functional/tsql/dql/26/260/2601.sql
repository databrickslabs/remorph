--Query type: DQL
WITH temp_result AS (SELECT 'customer' AS [Table Name])
SELECT FILEPROPERTY([Table Name], 'IsPrimaryFile') AS [Primary File]
FROM temp_result;