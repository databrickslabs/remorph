--Query type: DDL
DECLARE @MY_NEW_TABLE_NAME sysname = 'my_new_table';
WITH drop_table_query AS (
    SELECT 'DROP TABLE ' + QUOTENAME(@MY_NEW_TABLE_NAME) + ';' AS query
)
SELECT query FROM drop_table_query;
EXEC sp_executesql (SELECT query FROM drop_table_query);
-- REMORPH CLEANUP: DROP TABLE @MY_NEW_TABLE_NAME;