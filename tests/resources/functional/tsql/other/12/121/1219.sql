--Query type: DDL
CREATE TABLE Sales.UpdatedCustomer
(
    CustomerID INT NOT NULL,
    LocationID INT,
    NewBalance DECIMAL(10, 2),
    PreviousBalance DECIMAL(10, 2),
    CONSTRAINT PK_Customer PRIMARY KEY CLUSTERED (CustomerID, LocationID)
);

INSERT INTO Sales.UpdatedCustomer (CustomerID, LocationID, NewBalance, PreviousBalance)
SELECT CustomerID, LocationID, NewBalance, PreviousBalance
FROM (
    VALUES (1, 1, 100.00, 50.00),
           (2, 2, 200.00, 100.00)
) AS temp (CustomerID, LocationID, NewBalance, PreviousBalance);

SELECT * FROM Sales.UpdatedCustomer;
-- REMORPH CLEANUP: DROP TABLE Sales.UpdatedCustomer;