-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-endpoint-permissions-transact-sql?view=sql-server-ver16

USE master;  
DENY VIEW DEFINITION ON ENDPOINT::Mirror7 TO ZArifin;  
GO