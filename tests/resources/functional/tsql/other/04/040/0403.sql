--Query type: DDL
CREATE TABLE Sales.ZeroSales
(
    DeletedOrderID INT,
    RemovedOnDate DATETIME
);
-- REMORPH CLEANUP: DROP TABLE Sales.ZeroSales;