--Query type: DDL
CREATE TABLE Sales.NewCustomer
(
    CustomerID INT,
    CompanyName NVARCHAR(50),
    ContactName NVARCHAR(50),
    Phone NVARCHAR(20),
    AddressLine1 NVARCHAR(60),
    City NVARCHAR(30),
    Nation NVARCHAR(30),
    PostalCode NVARCHAR(15),
    CreditLimit DECIMAL(10, 2)
);

INSERT INTO Sales.NewCustomer
(
    CustomerID,
    CompanyName,
    ContactName,
    Phone,
    AddressLine1,
    City,
    Nation,
    PostalCode,
    CreditLimit
)
SELECT
    CustomerID,
    CompanyName,
    ContactName,
    Phone,
    AddressLine1,
    City,
    Nation,
    PostalCode,
    CreditLimit
FROM
(
    VALUES
    (
        1,
        'ABC Company',
        'John Doe',
        '123-456-7890',
        '123 Main St',
        'New York',
        'USA',
        '10001',
        1000.00
    )
) AS temp
(
    CustomerID,
    CompanyName,
    ContactName,
    Phone,
    AddressLine1,
    City,
    Nation,
    PostalCode,
    CreditLimit
);

SELECT * FROM Sales.NewCustomer;
-- REMORPH CLEANUP: DROP TABLE Sales.NewCustomer;
