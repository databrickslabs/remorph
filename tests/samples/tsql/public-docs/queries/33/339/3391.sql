-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/fulltextcatalogproperty-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT fulltextcatalogproperty('Cat_Desc', 'ItemCount');  
GO