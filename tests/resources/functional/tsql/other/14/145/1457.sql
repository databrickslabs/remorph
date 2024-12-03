--Query type: DML
SELECT TOP 100
    CustomerName,
    SalesAmount
FROM (
    SELECT
        CustomerName,
        SalesAmount,
        ROW_NUMBER() OVER (ORDER BY CustomerName) AS RowNum
    FROM (
        VALUES
            ('Customer1', 100.0),
            ('Customer2', 200.0),
            ('Customer3', 300.0),
            ('Customer4', 400.0),
            ('Customer5', 500.0),
            ('Customer6', 600.0)
    ) AS Sales (CustomerName, SalesAmount)
) AS subquery
WHERE CustomerName LIKE 'C%';
