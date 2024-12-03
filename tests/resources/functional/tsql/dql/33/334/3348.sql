--Query type: DQL
WITH temp_result AS (SELECT 'tpch_data' AS file_name)
SELECT FILE_IDEX(file_name) AS [File ID]
FROM temp_result;
