--Query type: DML
CREATE TABLE Customers
(
    CustomerID INT,
    CustomerName VARCHAR(50),
    Country VARCHAR(50)
);

INSERT INTO Customers
(
    CustomerID,
    CustomerName,
    Country
)
VALUES
(
    1,
    'John',
    'USA'
),
(
    2,
    'Alice',
    'Canada'
),
(
    3,
    'Bob',
    'Mexico'
);

DELETE FROM Customers
WHERE CustomerID = 2;

SELECT *
FROM Customers;

-- REMORPH CLEANUP: DROP TABLE Customers;