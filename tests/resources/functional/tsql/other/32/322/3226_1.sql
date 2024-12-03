--Query type: DCL
CREATE TABLE #Customers
(
    CustomerName VARCHAR(100),
    CustomerID INT
);

INSERT INTO #Customers
(
    CustomerName,
    CustomerID
)
VALUES
(
    'Customer1',
    100
),
(
    'Customer2',
    200
);

CREATE TABLE #Orders
(
    OrderName VARCHAR(100),
    OrderID INT
);

INSERT INTO #Orders
(
    OrderName,
    OrderID
)
VALUES
(
    'Order1',
    1000
),
(
    'Order2',
    2000
);

WITH CombinedData AS
(
    SELECT C.CustomerName, C.CustomerID, O.OrderName, O.OrderID
    FROM #Customers C
    CROSS JOIN #Orders O
)
SELECT *
FROM CombinedData;

DROP TABLE #Customers;

DROP TABLE #Orders;
