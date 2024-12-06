-- tsql sql:
SELECT *
FROM (
    VALUES
        (1, 'Customer1'),
        (2, 'Customer2')
) AS Customers (
    CustomerID,
    CustomerName
);
