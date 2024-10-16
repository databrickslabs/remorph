--Query type: DQL
WITH tables AS (
    SELECT name AS table_name
    FROM sys.tables
)
SELECT table_name
FROM tables;