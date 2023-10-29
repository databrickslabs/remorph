-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

SELECT ProductNumber,
    Name,
    "Price Range" = CASE
        WHEN ListPrice = 0 THEN 'Mfg item - not for resale'
        WHEN ListPrice < 50 THEN 'Under $50'
        WHEN ListPrice >= 50 AND ListPrice < 250 THEN 'Under $250'
        WHEN ListPrice >= 250 AND ListPrice < 1000 THEN 'Under $1000'
        ELSE 'Over $1000'
        END
FROM Production.Product
ORDER BY ProductNumber;
GO