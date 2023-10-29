-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql?view=sql-server-ver16

-- Create a synonym for the Product table in AdventureWorks2022.
CREATE SYNONYM MyProduct
FOR AdventureWorks2022.Production.Product;
GO

-- Query the Product table by using the synonym.
SELECT ProductID, Name
FROM MyProduct
WHERE ProductID < 5;
GO