-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-server-permissions-transact-sql?view=sql-server-ver16

USE master;  
DENY CREATE ENDPOINT TO ArifS AS MandarP;  
GO