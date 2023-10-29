-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/system-user-transact-sql?view=sql-server-ver16

DECLARE @sys_usr CHAR(30);  
SET @sys_usr = SYSTEM_USER;  
SELECT 'The current system user is: '+ @sys_usr;  
GO