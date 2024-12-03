--Query type: DML
CREATE TABLE #Orders
(
    OrderId INT,
    CustomerId INT,
    OrderDate DATE
);

INSERT INTO #Orders
(
    OrderId,
    CustomerId,
    OrderDate
)
VALUES
(
    10,
    1,
    '2020-01-01'
),
(
    20,
    2,
    '2020-01-15'
),
(
    30,
    3,
    '2020-02-01'
);

WITH OrdersCTE AS
(
    SELECT OrderId, CustomerId, OrderDate
    FROM #Orders
)
DELETE FROM OrdersCTE
WHERE OrderId = 10;

SELECT * FROM #Orders;

-- REMORPH CLEANUP: DROP TABLE #Orders;
