-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

-- Show byte counts with suffixes such as "KB", "MB", and "GB".
CREATE OR REPLACE FUNCTION NiceBytes(NUMBER_OF_BYTES INTEGER)
RETURNS VARCHAR
AS
$$
CASE
    WHEN NUMBER_OF_BYTES < 1024
        THEN NUMBER_OF_BYTES::VARCHAR
    WHEN NUMBER_OF_BYTES >= 1024 AND NUMBER_OF_BYTES < 1048576
        THEN (NUMBER_OF_BYTES / 1024)::VARCHAR || 'KB'
   WHEN NUMBER_OF_BYTES >= 1048576 AND NUMBER_OF_BYTES < (POW(2, 30))
       THEN (NUMBER_OF_BYTES / 1048576)::VARCHAR || 'MB'
    ELSE
        (NUMBER_OF_BYTES / POW(2, 30))::VARCHAR || 'GB'
END
$$
;
SHOW TABLES;
-- Show all of my tables in descending order of size.
SELECT "database_name", "schema_name", "name" as "table_name", NiceBytes("bytes") AS "size"
    FROM table(RESULT_SCAN(LAST_QUERY_ID()))
    ORDER BY "bytes" DESC;