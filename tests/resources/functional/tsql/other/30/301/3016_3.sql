-- tsql sql:
INSERT INTO tblCustomer (CustomerID, OrderTotal)
SELECT CustomerID, OrderTotal
FROM (
    VALUES
        (1, 100.00),
        (1, 200.00),
        (1, 50.00),
        (2, 75.00),
        (2, 125.00),
        (2, 150.00),
        (2, 150.00),
        (3, 25.00),
        (3, NULL),
        (4, NULL),
        (4, NULL)
) AS temp (CustomerID, OrderTotal);
