--Query type: DDL
CREATE TABLE #Suppliers
(
    SupplierID INT PRIMARY KEY NOT NULL,
    CompanyName VARCHAR(40) NOT NULL,
    ContactName VARCHAR(30) NULL,
    Address VARCHAR(60) NULL,
    City VARCHAR(15) NULL,
    PostalCode VARCHAR(10) NULL,
    Country VARCHAR(15) NULL,
    Phone VARCHAR(20) NULL
);

WITH SuppliersCTE AS
(
    SELECT
        SupplierID = 1,
        CompanyName = 'Supplier 1',
        ContactName = 'John Doe',
        Address = '123 Main St',
        City = 'New York',
        PostalCode = '10001',
        Country = 'USA',
        Phone = '123-456-7890'
)
INSERT INTO #Suppliers
(
    SupplierID,
    CompanyName,
    ContactName,
    Address,
    City,
    PostalCode,
    Country,
    Phone
)
SELECT
    SupplierID,
    CompanyName,
    ContactName,
    Address,
    City,
    PostalCode,
    Country,
    Phone
FROM SuppliersCTE;
