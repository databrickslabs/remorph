-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/objectproperty-transact-sql?view=sql-server-ver16

USE master;  
GO  
SELECT OBJECTPROPERTY(OBJECT_ID(N'AdventureWorks2022.HumanResources.vEmployee'), 'IsView');  
GO