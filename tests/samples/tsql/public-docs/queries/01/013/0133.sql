-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revert-transact-sql?view=sql-server-ver16

-- Sets the execution context of the session to 'login1'.  
EXECUTE AS LOGIN = 'login1';  
GO  
EXECUTE dbo.usp_myproc;