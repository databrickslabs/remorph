-- tsql sql:
SELECT o_orderkey AS [Order Key], c_custkey AS [Customer Key], o_orderdate AS [Order Date], c_name AS [Customer Name]
FROM (
    VALUES (1, 10, '2020-01-01', 'Customer1'),
           (2, 20, '2020-01-02', 'Customer2'),
           (3, 30, '2020-01-03', 'Customer3')
) AS orders (o_orderkey, c_custkey, o_orderdate, c_name)
ORDER BY o_orderkey;
