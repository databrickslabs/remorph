-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT IDENT_SEED('Person.Address') AS Identity_Seed;  
GO