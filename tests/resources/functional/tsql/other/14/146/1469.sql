--Query type: DCL
SELECT *
FROM (
    VALUES
        (1, 'Order1'),
        (2, 'Order2')
) AS OrderTVP (
    OrderID,
    OrderName
);
