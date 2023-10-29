-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-availability-group-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE VIEW DEFINITION ON AVAILABILITY GROUP::MyAg TO ZArifin;  
GO