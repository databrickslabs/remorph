-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT p.ProductID,
    v.BusinessEntityID
FROM Production.Product AS p
INNER JOIN Purchasing.ProductVendor AS v
    ON (p.ProductID = v.ProductID);