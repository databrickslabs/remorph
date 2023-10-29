-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-availability-group-permissions-transact-sql?view=sql-server-ver16

USE master;  
DENY VIEW DEFINITION ON AVAILABILITY GROUP::MyAg TO ZArifin;  
GO