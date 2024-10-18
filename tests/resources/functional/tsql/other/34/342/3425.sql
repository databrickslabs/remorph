--Query type: DML
CREATE TABLE SalesPerson
(
    BusinessEntityID INT,
    SalesYTD DECIMAL(10, 2)
);

CREATE TABLE SalesOrderHeader
(
    SalesPersonID INT,
    OrderDate DATE,
    SubTotal DECIMAL(10, 2)
);

INSERT INTO SalesPerson (BusinessEntityID, SalesYTD)
VALUES
    (1, 1000.00),
    (2, 2000.00),
    (3, 3000.00);

INSERT INTO SalesOrderHeader (SalesPersonID, OrderDate, SubTotal)
VALUES
    (1, '2022-01-01', 100.00),
    (1, '2022-01-15', 200.00),
    (2, '2022-02-01', 300.00),
    (3, '2022-03-01', 400.00);

WITH LatestOrders AS
(
    SELECT SalesPersonID, SubTotal, ROW_NUMBER() OVER (PARTITION BY SalesPersonID ORDER BY OrderDate DESC) AS RowNum
    FROM SalesOrderHeader
)
UPDATE sp
SET SalesYTD = SalesYTD + lo.SubTotal
FROM SalesPerson sp
JOIN LatestOrders lo ON sp.BusinessEntityID = lo.SalesPersonID
WHERE lo.RowNum = 1;

SELECT * FROM SalesPerson;
-- REMORPH CLEANUP: DROP TABLE SalesPerson;
-- REMORPH CLEANUP: DROP TABLE SalesOrderHeader;