-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/else-if-else-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
IF   
(SELECT COUNT(*) FROM Production.Product WHERE Name LIKE 'Touring-3000%' ) > 5  
PRINT 'There are more than 5 Touring-3000 bicycles.'  
ELSE PRINT 'There are 5 or less Touring-3000 bicycles.' ;  
GO