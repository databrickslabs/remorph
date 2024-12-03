--Query type: DML
WITH SalesOrderDetailCTE AS (
    SELECT ProductID, SUM(OrderQty) AS OrderQty
    FROM SalesOrderDetail AS sod
    INNER JOIN SalesOrderHeader AS soh ON sod.SalesOrderID = soh.SalesOrderID
    WHERE soh.OrderDate = '20070401'
    GROUP BY ProductID
)
MERGE ProductInventory AS pi
USING SalesOrderDetailCTE AS src
ON (pi.ProductID = src.ProductID)
WHEN MATCHED AND pi.Quantity - src.OrderQty <= 0
THEN DELETE
WHEN MATCHED
THEN UPDATE SET pi.Quantity = pi.Quantity - src.OrderQty
OUTPUT $ACTION, DELETED.ProductID, DELETED.Quantity AS OldQuantity, src.OrderQty AS NewQuantity
INTO #Changes(Action, ProductID, OldQuantity, NewQuantity);
INSERT INTO ZeroInventory (DeletedProductID, RemovedOnDate)
SELECT ProductID, GETDATE()
FROM #Changes
WHERE Action = 'DELETE';
SELECT * FROM ZeroInventory;
