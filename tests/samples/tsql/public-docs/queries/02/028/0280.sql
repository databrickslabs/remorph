-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/subtract-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT MAX(TaxRate) - MIN(TaxRate) AS 'Tax Rate Difference'  
FROM Sales.SalesTaxRate  
WHERE StateProvinceID IS NOT NULL;  
GO