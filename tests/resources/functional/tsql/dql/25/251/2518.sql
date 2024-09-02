--Query type: DQL
WITH db_info AS (
    SELECT 'my_database' AS db_name
)
SELECT DATABASEPROPERTYEX(db_name, 'IsAutoClose') AS auto_close_status
FROM db_info;