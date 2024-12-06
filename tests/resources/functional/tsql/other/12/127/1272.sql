-- tsql sql:
CREATE TABLE #OrderDetails
(
    OrderID int NOT NULL,
    ProductID int NOT NULL,
    UnitPrice decimal(10, 2) NULL,
    OrderQuantity smallint NULL,
    ReceivedQuantity float NULL,
    RejectedQuantity float NULL,
    DueDate datetime NULL,
    rowguid uniqueidentifier ROWGUIDCOL NOT NULL
        CONSTRAINT DF_OrderDetails_rowguid DEFAULT (NEWID()),
    ModifiedDate datetime NOT NULL
        CONSTRAINT DF_OrderDetails_ModifiedDate DEFAULT (GETDATE()),
    LineTotal AS (UnitPrice * OrderQuantity),
    StockedQuantity AS (ReceivedQuantity - RejectedQuantity),
    CONSTRAINT PK_OrderDetails_OrderID_ProductID
        PRIMARY KEY CLUSTERED (OrderID, ProductID)
        WITH (IGNORE_DUP_KEY = OFF)
);

INSERT INTO #OrderDetails (OrderID, ProductID, UnitPrice, OrderQuantity, ReceivedQuantity, RejectedQuantity, DueDate)
SELECT
    O.OrderID,
    P.ProductID,
    CAST(10.99 AS decimal(10, 2)),
    10,
    10.0,
    0.0,
    GETDATE()
FROM (VALUES (1), (2), (3)) AS O(OrderID)
CROSS JOIN (VALUES (1), (2), (3)) AS P(ProductID);

SELECT * FROM #OrderDetails;

DROP TABLE #OrderDetails;
