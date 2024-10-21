--Query type: DQL
WITH EmployeeCTE AS (
    SELECT CustomerID, AccountNumber, OrderDate, ShipDate
    FROM (
        VALUES
            (1, '12345', '2020-01-01', '2020-01-05'),
            (2, '67890', '2020-01-15', '2020-01-20')
    ) AS Employee (CustomerID, AccountNumber, OrderDate, ShipDate)
)
SELECT CustomerID, AccountNumber, OrderDate, ShipDate
FROM EmployeeCTE
WHERE AccountNumber < '50000';