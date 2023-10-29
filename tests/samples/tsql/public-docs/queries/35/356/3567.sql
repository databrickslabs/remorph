-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-availability-group-permissions-transact-sql?view=sql-server-ver16

USE master;  
GRANT VIEW DEFINITION ON AVAILABILITY GROUP::MyAg TO ZArifin;  
GO