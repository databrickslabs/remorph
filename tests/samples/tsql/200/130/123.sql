SELECT p.ProductID,
    v.BusinessEntityID
FROM Production.Product AS p
INNER JOIN Purchasing.ProductVendor AS v
    ON (p.ProductID = v.ProductID);