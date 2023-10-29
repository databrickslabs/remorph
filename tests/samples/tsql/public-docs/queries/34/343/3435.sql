-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-system-object-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GRANT SELECT ON sys.sql_logins TO Sylvester1;  
GRANT VIEW SERVER STATE to Sylvester1;  
GO