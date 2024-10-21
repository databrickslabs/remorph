--Query type: DQL
DECLARE tables CURSOR FOR
WITH temp_table AS (
    SELECT TABLE_SCHEMA + '.' + TABLE_NAME AS table_name, TABLE_TYPE, CASE WHEN TABLE_TYPE = 'BASE TABLE' THEN 'Base Table' WHEN TABLE_TYPE = 'VIEW' THEN 'View' ELSE 'Other' END AS table_type_description
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE IN ('BASE TABLE', 'VIEW')
)
SELECT table_name, table_type, table_type_description FROM temp_table;