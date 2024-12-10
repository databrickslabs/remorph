-- tsql sql:
CREATE TABLE #Orders
(
    OrderKey INT,
    OrderStatus VARCHAR(50)
);

INSERT INTO #Orders
(
    OrderKey,
    OrderStatus
)
VALUES
(
    1,
    'Shipped'
),
(
    2,
    'Pending'
),
(
    3,
    'Shipped'
);

WITH LargeOrders AS
(
    SELECT OrderKey, Quantity
    FROM
    (
        VALUES
        (
            1,
            1,
            2
        ),
        (
            1,
            2,
            3
        ),
        (
            2,
            1,
            1
        ),
        (
            3,
            1,
            4
        )
    ) AS LineItems
    (
        OrderKey,
        LineItemKey,
        Quantity
    )
    WHERE Quantity > 2
)
UPDATE o
SET o.OrderStatus += ' - large order'
FROM #Orders o
JOIN LargeOrders lo ON o.OrderKey = lo.OrderKey;

SELECT * FROM #Orders;
