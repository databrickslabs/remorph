--Query type: DQL
SELECT o_orderdate, SUM(o_totalprice) AS TotalSales
FROM (
    VALUES
        (1, '1996-01-01', 100.00),
        (2, '1996-01-02', 200.00),
        (3, '1996-01-03', 300.00),
        (4, '1996-01-04', 400.00),
        (5, '1996-01-05', 500.00)
) AS orders (o_orderkey, o_orderdate, o_totalprice)
GROUP BY o_orderdate
ORDER BY o_orderdate;