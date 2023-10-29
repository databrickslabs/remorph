-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-schema-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
ALTER SCHEMA HumanResources TRANSFER Person.Address;  
GO