-- tsql sql:
DROP TABLE IF EXISTS tempCustomer;
SELECT *
FROM (
    VALUES (
        1, 'John Smith', 'USA',
        2, 'Jane Smith', 'Canada'
    )
) AS tempCustomer (
    CustomerID,
    Name,
    Country
);
