-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql?view=sql-server-ver16

SELECT
    resource_type, resource_database_id, request_mode, request_type, request_status, request_session_id 
FROM 
    sys.dm_tran_locks
WHERE
    resource_database_id = DB_ID('testdb');