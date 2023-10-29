-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

IF OBJECT_ID(N'Production.ZeroInventory', N'U') IS NOT NULL
    DROP TABLE Production.ZeroInventory;
GO

--Create ZeroInventory table.
CREATE TABLE Production.ZeroInventory (
    DeletedProductID INT,
    RemovedOnDate DATETIME
    );
GO

INSERT INTO Production.ZeroInventory (
    DeletedProductID,
    RemovedOnDate
)
SELECT ProductID,
    GETDATE()
FROM (
    MERGE Production.ProductInventory AS pi
    USING (
        SELECT ProductID,
            SUM(OrderQty)
        FROM Sales.SalesOrderDetail AS sod
        INNER JOIN Sales.SalesOrderHeader AS soh
            ON sod.SalesOrderID = soh.SalesOrderID
                AND soh.OrderDate = '20070401'
        GROUP BY ProductID
        ) AS src(ProductID, OrderQty)
        ON (pi.ProductID = src.ProductID)
    WHEN MATCHED
        AND pi.Quantity - src.OrderQty <= 0
        THEN
            DELETE
    WHEN MATCHED
        THEN
            UPDATE
            SET pi.Quantity = pi.Quantity - src.OrderQty
    OUTPUT $ACTION,
        DELETED.ProductID
    ) AS Changes(Action, ProductID)
WHERE Action = 'DELETE';

IF @@ROWCOUNT = 0
    PRINT 'Warning: No rows were inserted';
GO

SELECT DeletedProductID,
    RemovedOnDate
FROM Production.ZeroInventory;
GO