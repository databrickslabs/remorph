--Query type: DML
WITH SalesOrderTemp AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, '2020-01-01', 100.00),
            (1001, 2, '2020-01-02', 200.00),
            (2001, 3, '2020-01-03', 300.00),
            (3001, 4, '2020-01-04', 400.00),
            (5001, 6, '2020-01-06', 600.00)
    ) AS V (OrderID, CustomerID, OrderDate, TotalCost)
)
SELECT *
FROM SalesOrderTemp;
