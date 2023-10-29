-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-endpoint-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE VIEW DEFINITION ON ENDPOINT::Mirror7 FROM ZArifin;  
GO