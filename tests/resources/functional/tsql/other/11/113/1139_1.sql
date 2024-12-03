--Query type: DDL
CREATE TABLE [HR].[Orders]
(
    OrderID INT NOT NULL,
    OrderDate DATE NOT NULL,
    ProductID INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    Quantity INT NOT NULL,
    CategoryID INT NOT NULL,
    CategoryName VARCHAR(50) NOT NULL
)
WITH (SYSTEM_VERSIONING = ON, LEDGER = ON);

WITH TempResult AS
(
    SELECT 1 AS OrderID, '1996-07-01' AS OrderDate, 1 AS ProductID, 10.0 AS UnitPrice, 2 AS Quantity, 1 AS CategoryID, 'Category1' AS CategoryName
    UNION ALL
    SELECT 2, '1996-07-02', 2, 20.0, 3, 2, 'Category2'
    UNION ALL
    SELECT 3, '1996-07-03', 3, 30.0, 4, 3, 'Category3'
)
INSERT INTO [HR].[Orders]
SELECT * FROM TempResult;

SELECT OrderID, OrderDate, ProductID, UnitPrice, Quantity, CategoryID, CategoryName
FROM (
    VALUES (1, '1996-07-01', 1, 10.0, 2, 1, 'Category1'),
    (2, '1996-07-02', 2, 20.0, 3, 2, 'Category2'),
    (3, '1996-07-03', 3, 30.0, 4, 3, 'Category3')
) AS DerivedTable(OrderID, OrderDate, ProductID, UnitPrice, Quantity, CategoryID, CategoryName)
WHERE OrderDate >= '1996-07-01' AND OrderDate < '1996-08-01'
GROUP BY OrderID, OrderDate, ProductID, UnitPrice, Quantity, CategoryID, CategoryName
HAVING SUM(UnitPrice * Quantity) > 1000
ORDER BY OrderID, OrderDate;
