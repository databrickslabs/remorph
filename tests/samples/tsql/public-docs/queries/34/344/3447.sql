-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-database-principal-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
REVOKE IMPERSONATE ON USER::HamithaL FROM AccountsPayable17;  
GO