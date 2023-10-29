-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-availability-group-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE TAKE OWNERSHIP ON AVAILABILITY GROUP::MyAg TO PKomosinski   
    CASCADE;  
GO