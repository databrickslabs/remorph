-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-server-principal-permissions-transact-sql?view=sql-server-ver16

USE master;  
DENY VIEW DEFINITION ON SERVER ROLE::Sales TO Auditors ;  
GO