-- tsql sql:
CREATE TABLE Customer
(
    CustomerID INT,
    CustomerName VARCHAR(50),
    Address VARCHAR(100)
);

INSERT INTO Customer (CustomerID, CustomerName, Address)
VALUES
    (1, 'John Doe', '123 Main St'),
    (2, 'Jane Doe', '456 Elm St'),
    (3, 'Bob Smith', '789 Oak St');

UPDATE STATISTICS Customer (CustomerID);

SELECT *
FROM Customer;

-- REMORPH CLEANUP: DROP TABLE Customer;
