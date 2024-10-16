--Query type: DDL
CREATE TABLE dbo.CustomerOrders
(
    CustomerID INT,
    OrderDate DATE,
    TotalCost DECIMAL(10, 2)
);
-- REMORPH CLEANUP: DROP TABLE dbo.CustomerOrders;