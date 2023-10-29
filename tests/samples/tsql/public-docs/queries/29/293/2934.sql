-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT p.Name AS ProductName,
    v.Name AS VendorName
FROM Production.Product AS p
INNER MERGE JOIN Purchasing.ProductVendor AS pv
    ON p.ProductID = pv.ProductID
INNER HASH JOIN Purchasing.Vendor AS v
    ON pv.BusinessEntityID = v.BusinessEntityID
ORDER BY p.Name,
    v.Name;