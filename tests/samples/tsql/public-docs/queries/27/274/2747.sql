-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/spid-transact-sql?view=sql-server-ver16

SELECT SESSION_ID() AS ID, @@SPID AS 'Control ID', SYSTEM_USER AS 'Login Name', USER AS 'User Name';