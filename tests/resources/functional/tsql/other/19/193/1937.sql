--Query type: DML
DECLARE @OrderDetails TABLE (OrderKey INT, TotalPrice DECIMAL(10, 2));
INSERT INTO @OrderDetails (OrderKey, TotalPrice)
VALUES
    (1, 100.0),
    (2, 200.0),
    (3, 300.0),
    (4, 400.0),
    (5, 500.0),
    (6, 600.0),
    (7, 700.0),
    (8, 800.0),
    (9, 900.0),
    (10, 1000.0);
DELETE FROM @OrderDetails
WHERE OrderKey IN (
    SELECT TOP 10 OrderKey
    FROM @OrderDetails
    ORDER BY TotalPrice ASC
);
SELECT *
FROM @OrderDetails;
