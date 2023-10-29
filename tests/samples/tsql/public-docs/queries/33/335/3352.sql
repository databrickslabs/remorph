-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-current-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT IDENT_CURRENT ('Person.Address') AS Current_Identity;  
GO