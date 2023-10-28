USE AdventureWorks2022;  
GO  
DECLARE @SearchWord VARCHAR(30)  
SET @SearchWord ='performance'  
SELECT Description   
FROM Production.ProductDescription   
WHERE FREETEXT(Description, @SearchWord);