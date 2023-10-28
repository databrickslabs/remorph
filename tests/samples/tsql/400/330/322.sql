CREATE TABLE Production.UpdatedInventory (
    ProductID INT NOT NULL,
    LocationID INT,
    NewQty INT,
    PreviousQty INT,
    CONSTRAINT PK_Inventory PRIMARY KEY CLUSTERED (
        ProductID,
        LocationID
        )
    );
GO

INSERT INTO Production.UpdatedInventory
SELECT ProductID, LocationID, NewQty, PreviousQty
FROM (
    MERGE Production.ProductInventory AS pi
    USING (
        SELECT ProductID, SUM(OrderQty)
        FROM Sales.SalesOrderDetail AS sod
        INNER JOIN Sales.SalesOrderHeader AS soh
            ON sod.SalesOrderID = soh.SalesOrderID
                AND soh.OrderDate BETWEEN '20030701'
                    AND '20030731'
        GROUP BY ProductID
        ) AS src(ProductID, OrderQty)
        ON pi.ProductID = src.ProductID
    WHEN MATCHED
        AND pi.Quantity - src.OrderQty >= 0
        THEN
            UPDATE SET pi.Quantity = pi.Quantity - src.OrderQty
    WHEN MATCHED
        AND pi.Quantity - src.OrderQty <= 0
        THEN
            DELETE
    OUTPUT $action,
        Inserted.ProductID,
        Inserted.LocationID,
        Inserted.Quantity AS NewQty,
        Deleted.Quantity AS PreviousQty
    ) AS Changes(Action, ProductID, LocationID, NewQty, PreviousQty)
WHERE Action = 'UPDATE';
GO