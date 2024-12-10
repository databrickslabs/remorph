-- tsql sql:
CREATE PROCEDURE #usp_UpdateOrderStatus
    @OrderDate DATETIME
AS
BEGIN
    MERGE #SalesOrder AS tgt
    USING (
        SELECT OrderID, SUM(UnitPrice * Quantity) AS TotalRevenue
        FROM (
            VALUES (1, 10.0, 2),
                   (2, 20.0, 3),
                   (3, 30.0, 1)
        ) AS OrderDetails(OrderID, UnitPrice, Quantity)
        INNER JOIN (
            VALUES (1, 100.0, GETDATE()),
                   (2, 200.0, GETDATE()),
                   (3, 300.0, GETDATE())
        ) AS SalesOrder(srcOrderID, srcTotalRevenue, srcModifiedDate)
            ON OrderDetails.OrderID = SalesOrder.srcOrderID
        GROUP BY OrderDetails.OrderID
    ) AS src
    ON (tgt.OrderID = src.OrderID)
    WHEN MATCHED AND tgt.TotalRevenue - src.TotalRevenue <= 0 THEN
        DELETE
    WHEN MATCHED THEN
        UPDATE SET tgt.TotalRevenue = tgt.TotalRevenue - src.TotalRevenue,
                     tgt.ModifiedDate = GETDATE()
    OUTPUT $action, Inserted.OrderID, Inserted.TotalRevenue, Inserted.ModifiedDate, Deleted.OrderID, Deleted.TotalRevenue, Deleted.ModifiedDate;
END;

CREATE TABLE #SalesOrder (
    OrderID INT,
    TotalRevenue DECIMAL(10, 2),
    ModifiedDate DATETIME
);

EXEC #usp_UpdateOrderStatus '2023-01-01';

SELECT * FROM #SalesOrder;

-- REMORPH CLEANUP: DROP TABLE #SalesOrder;
-- REMORPH CLEANUP: DROP PROCEDURE #usp_UpdateOrderStatus;
