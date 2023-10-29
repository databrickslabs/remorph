-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/freetext-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
DECLARE @SearchWord NVARCHAR(30)  
SET @SearchWord = N'performance'  
SELECT Description   
FROM Production.ProductDescription   
WHERE FREETEXT(Description, @SearchWord);