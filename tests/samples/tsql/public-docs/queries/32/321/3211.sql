-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-database-principal-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
DENY VIEW DEFINITION ON ROLE::SammamishParking   
    TO JinghaoLiu CASCADE;  
GO