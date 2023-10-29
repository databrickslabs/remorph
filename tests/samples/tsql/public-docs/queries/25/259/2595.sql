-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT EnglishProductName AS Name, ListPrice
FROM dbo.DimProduct
WHERE CAST(CAST(ListPrice AS INT) AS CHAR(20)) LIKE '2%';