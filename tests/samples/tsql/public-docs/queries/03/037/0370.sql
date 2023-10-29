-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/rename-transact-sql?view=aps-pdw-2016-au7

-- View a list of the current sessions
SELECT session_id, login_name, status
FROM sys.dm_pdw_exec_sessions
WHERE status='Active' OR status='Idle';

-- Terminate a session using the session_id.
KILL 'SID1234';