--Query type: DML
CREATE TABLE Sales.NewCustomer
(
    CustID INT,
    LastName VARCHAR(50),
    FirstName VARCHAR(50),
    Phone VARCHAR(25),
    Address VARCHAR(100),
    City VARCHAR(50),
    StateProvince VARCHAR(50),
    PostalCode VARCHAR(10),
    CurrentFlag BIT
);

WITH CustomerTemp (CustID, LastName, FirstName, Phone, Address, City, StateProvince, PostalCode, CurrentFlag)
AS
(
    SELECT c.CustomerID, c.LastName, c.FirstName, pp.PhoneNumber, a.AddressLine1, a.City, sp.StateProvinceCode, a.PostalCode, c.CurrentFlag
    FROM
    (
        SELECT CustomerID, LastName, FirstName, CurrentFlag
        FROM Sales.Customer
    ) c
    INNER JOIN
    (
        SELECT CustomerID, AddressID
        FROM Sales.CustomerAddress
    ) ca
    ON c.CustomerID = ca.CustomerID
    INNER JOIN
    (
        SELECT AddressID, AddressLine1, City, StateProvinceID, PostalCode
        FROM Sales.Address
    ) a
    ON ca.AddressID = a.AddressID
    INNER JOIN
    (
        SELECT StateProvinceID, StateProvinceCode
        FROM Sales.StateProvince
    ) sp
    ON a.StateProvinceID = sp.StateProvinceID
    INNER JOIN
    (
        SELECT BusinessEntityID, PhoneNumber
        FROM Sales.PersonPhone
    ) pp
    ON c.CustomerID = pp.BusinessEntityID
)
INSERT INTO Sales.NewCustomer
SELECT CustID, LastName, FirstName, Phone, Address, City, StateProvince, PostalCode, CurrentFlag
FROM CustomerTemp;