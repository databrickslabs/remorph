SELECT p.Name,
    sod.SalesOrderID
FROM Production.Product AS p
LEFT OUTER JOIN Sales.SalesOrderDetail AS sod
    ON p.ProductID = sod.ProductID
ORDER BY p.Name;