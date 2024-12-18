-- tsql sql:
SELECT COUNT(*) AS TotalOrders
FROM (
    VALUES
        (1, '2020-01-01', 100.00),
        (2, '2020-01-02', 200.00),
        (3, '2020-01-03', 300.00)
) AS Orders (
    OrderKey,
    OrderDate,
    TotalPrice
);
