-- tsql sql:
SELECT *
INTO NewOrderTable
FROM (
    VALUES
        (1, 'Order1', 100.0),
        (2, 'Order2', 200.0),
        (3, 'Order3', 300.0)
) AS OrderData (
    OrderID,
    OrderName,
    OrderTotal
);
