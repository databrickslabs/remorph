-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/user-name-transact-sql?view=sql-server-ver16

SELECT name FROM sys.database_principals WHERE name = USER_NAME(1);  
GO