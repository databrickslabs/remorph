-- tsql sql:
DECLARE @MyTableVar TABLE (
    OrderID INT NOT NULL,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    TotalDue MONEY NOT NULL,
    Freight MONEY NOT NULL
);

WITH SalesData AS (
    SELECT soh.SalesOrderID,
        soh.CustomerID,
        soh.OrderDate,
        soh.TotalDue,
        soh.Freight,
        c.AccountNumber
    FROM (
        VALUES
            (43670, 1, '2011-05-31', 1378.0862, 12.4862, 'AW000001'),
            (43669, 2, '2011-05-30', 514.7912, 89.7912, 'AW000002'),
            (43668, 3, '2011-05-27', 1516.1396, 48.1396, 'AW000003'),
            (43667, 4, '2011-05-25', 943.8784, 24.8784, 'AW000004'),
            (43666, 5, '2011-05-23', 1271.4654, 14.4654, 'AW000005')
    ) AS soh (SalesOrderID, CustomerID, OrderDate, TotalDue, Freight, AccountNumber)
    INNER JOIN (
        VALUES
            ('AW000001', 'Customer 1'),
            ('AW000002', 'Customer 2'),
            ('AW000003', 'Customer 3'),
            ('AW000004', 'Customer 4'),
            ('AW000005', 'Customer 5')
    ) AS c (AccountNumber, CustomerName)
    ON soh.AccountNumber = c.AccountNumber
)
INSERT INTO @MyTableVar
OUTPUT INSERTED.OrderID,
    INSERTED.CustomerID,
    INSERTED.OrderDate,
    INSERTED.TotalDue,
    INSERTED.Freight
SELECT SalesOrderID,
    CustomerID,
    OrderDate,
    TotalDue,
    Freight
FROM SalesData
WHERE SalesOrderID LIKE '5%'
ORDER BY OrderDate,
    CustomerID;
