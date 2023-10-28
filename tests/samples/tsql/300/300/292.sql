USE AdventureWorks2022;  
GO  
DECLARE @NewPrice INT = 10;  
UPDATE Production.Product  
SET ListPrice += @NewPrice  
WHERE Color = N'Red';  
GO