-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-server-principal-permissions-transact-sql?view=sql-server-ver16

USE master;  
GRANT VIEW DEFINITION ON LOGIN::EricKurjan TO RMeyyappan   
    WITH GRANT OPTION;  
GO