-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openjson-transact-sql?view=sql-server-ver16

SELECT *
FROM products
WHERE product.productTypeID IN (1,2,3,4)