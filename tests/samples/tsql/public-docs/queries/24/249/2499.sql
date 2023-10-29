-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/current-user-transact-sql?view=sql-server-ver16

SELECT CURRENT_USER;  
GO  
EXECUTE AS USER = 'Arnalfo';  
GO  
SELECT CURRENT_USER;  
GO  
REVERT;  
GO  
SELECT CURRENT_USER;  
GO