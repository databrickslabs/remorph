-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-object-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
REVOKE SELECT ON OBJECT::Person.Address FROM RosaQdM;  
GO