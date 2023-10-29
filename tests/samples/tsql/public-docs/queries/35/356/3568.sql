-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-endpoint-permissions-transact-sql?view=sql-server-ver16

USE master;  
GRANT VIEW DEFINITION ON ENDPOINT::Mirror7 TO ZArifin;  
GO