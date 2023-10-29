-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-endpoint-permissions-transact-sql?view=sql-server-ver16

USE master;  
GRANT TAKE OWNERSHIP ON ENDPOINT::Shipping83 TO PKomosinski   
    WITH GRANT OPTION;  
GO