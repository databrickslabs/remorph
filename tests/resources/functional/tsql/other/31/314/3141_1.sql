--Query type: DML
CREATE TABLE Sales.SalesOrderHeader
(
    RevisionNumber INT,
    Status INT,
    EmployeeID INT,
    VendorID INT,
    ShipMethodID INT,
    OrderDate DATETIME,
    ShipDate DATETIME,
    SubTotal DECIMAL(18, 2),
    TaxAmt DECIMAL(18, 2),
    Freight DECIMAL(18, 2)
);

INSERT INTO Sales.SalesOrderHeader
(
    RevisionNumber,
    Status,
    EmployeeID,
    VendorID,
    ShipMethodID,
    OrderDate,
    ShipDate,
    SubTotal,
    TaxAmt,
    Freight
)
SELECT
    RevisionNumber,
    Status,
    EmployeeID,
    VendorID,
    ShipMethodID,
    OrderDate,
    ShipDate,
    SubTotal,
    TaxAmt,
    Freight
FROM
(
    VALUES
    (
        2,
        3,
        261,
        1652,
        4,
        GETDATE(),
        GETDATE(),
        44594.55,
        3567.56,
        1114.86
    )
) AS SalesData
(
    RevisionNumber,
    Status,
    EmployeeID,
    VendorID,
    ShipMethodID,
    OrderDate,
    ShipDate,
    SubTotal,
    TaxAmt,
    Freight
);

SELECT * FROM Sales.SalesOrderHeader;
