-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-incr-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT IDENT_INCR('Person.Address') AS Identity_Increment;  
GO