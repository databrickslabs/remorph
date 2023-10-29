-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT EnglishProductName AS ProductName, ListPrice
FROM dbo.DimProduct
WHERE CAST(ListPrice AS int) LIKE '3%';