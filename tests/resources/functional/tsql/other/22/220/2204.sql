--Query type: DML
CREATE TABLE SalesPerson
(
    BusinessEntityID INT,
    SalesYTD DECIMAL(10, 2)
);

CREATE TABLE Person
(
    BusinessEntityID INT,
    LastName VARCHAR(50),
    FirstName VARCHAR(50)
);

INSERT INTO SalesPerson (BusinessEntityID, SalesYTD)
VALUES
    (1, 300000.00),
    (2, 200000.00),
    (3, 400000.00),
    (4, 100000.00),
    (5, 500000.00);

INSERT INTO Person (BusinessEntityID, LastName, FirstName)
VALUES
    (1, 'Smith', 'John'),
    (2, 'Johnson', 'Mike'),
    (3, 'Williams', 'Emma'),
    (4, 'Jones', 'David'),
    (5, 'Brown', 'Sophia');

CREATE TABLE EmployeeSales
(
    EmployeeID INT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    YearlySales DECIMAL(10, 2)
);

WITH SalesData AS
(
    SELECT TOP (5) sp.BusinessEntityID, p.LastName, p.FirstName, sp.SalesYTD
    FROM SalesPerson sp
    INNER JOIN Person p ON sp.BusinessEntityID = p.BusinessEntityID
    WHERE sp.SalesYTD > 250000.00
    ORDER BY sp.SalesYTD DESC
)
INSERT INTO EmployeeSales (EmployeeID, FirstName, LastName, YearlySales)
OUTPUT inserted.EmployeeID, inserted.FirstName, inserted.LastName, inserted.YearlySales
SELECT BusinessEntityID, FirstName, LastName, SalesYTD
FROM SalesData;

SELECT *
FROM EmployeeSales;

-- REMORPH CLEANUP: DROP TABLE SalesPerson;
-- REMORPH CLEANUP: DROP TABLE Person;
-- REMORPH CLEANUP: DROP TABLE EmployeeSales;