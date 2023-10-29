-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/deallocate-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
  
DECLARE @MyCursor CURSOR;  
SET @MyCursor = CURSOR LOCAL SCROLL FOR  
    SELECT * FROM Sales.SalesPerson;  
  
DEALLOCATE @MyCursor;  
  
SET @MyCursor = CURSOR LOCAL SCROLL FOR  
    SELECT * FROM Sales.SalesTerritory;  
GO