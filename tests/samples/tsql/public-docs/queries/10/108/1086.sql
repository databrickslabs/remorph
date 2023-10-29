-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

CREATE PROCEDURE Production.usp_UpdateInventory @OrderDate DATETIME
AS
MERGE Production.ProductInventory AS tgt
USING (
    SELECT ProductID,
        SUM(OrderQty)
    FROM Sales.SalesOrderDetail AS sod
    INNER JOIN Sales.SalesOrderHeader AS soh
        ON sod.SalesOrderID = soh.SalesOrderID
            AND soh.OrderDate = @OrderDate
    GROUP BY ProductID
    ) AS src(ProductID, OrderQty)
    ON (tgt.ProductID = src.ProductID)
WHEN MATCHED
    AND tgt.Quantity - src.OrderQty <= 0
    THEN
        DELETE
WHEN MATCHED
    THEN
        UPDATE
        SET tgt.Quantity = tgt.Quantity - src.OrderQty,
            tgt.ModifiedDate = GETDATE();
GO

EXECUTE Production.usp_UpdateInventory '20030501';