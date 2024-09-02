--Query type: DDL
CREATE TABLE CustomerOrders
(
    CustomerID INT IDENTITY(1, 5) NOT NULL,
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    ProjectedAmount AS TotalAmount * 1.10
);

WITH CustomerOrdersCTE AS
(
    SELECT 1 AS CustomerID, CAST('2023-01-01' AS DATE) AS OrderDate, 100.00 AS TotalAmount
)
INSERT INTO CustomerOrders (CustomerID, OrderDate, TotalAmount)
SELECT CustomerID, OrderDate, TotalAmount
FROM CustomerOrdersCTE;

SELECT *
FROM CustomerOrders;
-- REMORPH CLEANUP: DROP TABLE CustomerOrders;