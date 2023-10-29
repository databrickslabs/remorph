-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/not-equal-to-transact-sql-traditional?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT ProductCategoryID, Name  
FROM Production.ProductCategory  
WHERE ProductCategoryID <> 3 AND ProductCategoryID <> 2;