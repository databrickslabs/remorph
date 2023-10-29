-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-endpoint-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE TAKE OWNERSHIP ON ENDPOINT::Shipping83 FROM PKomosinski   
    CASCADE;  
GO