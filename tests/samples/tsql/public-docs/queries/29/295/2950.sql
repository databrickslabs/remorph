-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-outputbuffer-transact-sql?view=sql-server-ver16

SELECT request_id
FROM sys.dm_exec_requests
WHERE session_id = @@spid;