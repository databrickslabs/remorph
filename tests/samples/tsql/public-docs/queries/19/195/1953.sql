-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-system-object-permissions-transact-sql?view=sql-server-ver16

DENY EXECUTE ON sys.xp_cmdshell TO public;  
GO