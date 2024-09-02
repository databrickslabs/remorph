--Query type: DML
CREATE TABLE Orders (
    OrderKey INT PRIMARY KEY,
    OrderStatus VARCHAR(10),
    TotalPrice DECIMAL(10, 2)
);

WITH TempResult AS (
    SELECT OrderKey, OrderStatus, TotalPrice
    FROM (
        VALUES (
            (1, 'OPEN', 100.00),
            (2, 'CLOSED', 200.00),
            (3, 'OPEN', 300.00)
        )
    ) AS Orders (OrderKey, OrderStatus, TotalPrice)
)
INSERT INTO Orders
SELECT OrderKey, OrderStatus, TotalPrice
FROM TempResult;

SELECT OrderStatus
FROM (
    VALUES (
        (1, 'OPEN', 100.00),
        (2, 'CLOSED', 200.00),
        (3, 'OPEN', 300.00)
    )
) AS Orders (OrderKey, OrderStatus, TotalPrice)
WHERE OrderKey = 1;