--Query type: DQL
WITH temp_result AS (
    SELECT file_name, file_size, last_modified, uploaded_by
    FROM sys.master_files
    WHERE database_id = DB_ID('mydb')
        AND file_id = 1
        AND modified_date > DATEADD(hour, -1, GETDATE())
)
SELECT *
FROM temp_result;