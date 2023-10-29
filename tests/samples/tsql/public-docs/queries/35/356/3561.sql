-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-availability-group-permissions-transact-sql?view=sql-server-ver16

USE master;  
GRANT CONTROL ON AVAILABILITY GROUP::MyAg TO PKomosinski   
    WITH GRANT OPTION;  
GO  
REVOKE GRANT OPTION FOR CONTROL ON AVAILABILITY GROUP::MyAg TO PKomosinski  
CASCADE  
GO