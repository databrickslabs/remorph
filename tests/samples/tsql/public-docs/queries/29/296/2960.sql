-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-array-transact-sql?view=sql-server-ver16

SELECT s.session_id, JSON_ARRAY(s.host_name, s.program_name, s.client_interface_name)
FROM sys.dm_exec_sessions AS s
WHERE s.is_user_process = 1;