--Query type: DDL
CREATE TABLE Customer
(
    CustomerKey INT NOT NULL PRIMARY KEY,
    CustomerName VARCHAR(50) NOT NULL,
    SalesPersonID INT NULL,
    Address VARCHAR(100) NULL,
    ValidFrom DATETIME2 NOT NULL DEFAULT GETDATE(),
    ValidTo DATETIME2 NOT NULL DEFAULT '9999-12-31 23:59:59.9999999'
);

WITH CustomerCTE AS
(
    SELECT
        CustomerKey = 1,
        CustomerName = 'John Doe',
        SalesPersonID = 1,
        Address = '123 Main St'
)
INSERT INTO Customer
(
    CustomerKey,
    CustomerName,
    SalesPersonID,
    Address
)
SELECT
    CustomerKey,
    CustomerName,
    SalesPersonID,
    Address
FROM CustomerCTE;

SELECT * FROM Customer;
-- REMORPH CLEANUP: DROP TABLE Customer;
