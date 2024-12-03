--Query type: DML
WITH Lineitem AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES (1, 10.0, 0.1),
               (2, 20.0, 0.2),
               (3, 30.0, 0.3)
    ) AS Lineitem(l_orderkey, l_extendedprice, l_discount)
)
SELECT 'The total revenue as of ' + CAST(GETDATE() AS CHAR(20)) + ' is ' + CAST(SUM(l_extendedprice * l_discount) AS CHAR(10)) AS TotalRevenue
FROM Lineitem;
