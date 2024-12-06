-- tsql sql:
WITH CustomerCTE AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 1, 1),
            (2, 2, 2, 2)
    ) AS Customer (
        CustomerKey,
        OrderDateKey,
        DueDateKey,
        ShipDateKey
    )
)
SELECT *
FROM CustomerCTE;
