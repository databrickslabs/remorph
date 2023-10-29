-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/objectproperty-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT OBJECTPROPERTY(OBJECT_ID('dbo.ufnGetProductDealerPrice'), 'IsDeterministic');  
GO