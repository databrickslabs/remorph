-- The OUTER keyword following the FULL keyword is optional.
SELECT p.Name,
    sod.SalesOrderID
FROM Production.Product AS p
FULL JOIN Sales.SalesOrderDetail AS sod
    ON p.ProductID = sod.ProductID
ORDER BY p.Name;