-- tsql sql:
WITH SalesCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice, ROW_NUMBER() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS RowNum,
    RANK() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS Rank,
    DENSE_RANK() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS DenseRank
    FROM (
        VALUES (1, 1, 100.0),
        (2, 1, 200.0),
        (3, 2, 50.0),
        (4, 2, 75.0),
        (5, 3, 150.0)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
),
CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'John Smith', '123 Main St'),
        (2, 'Jane Doe', '456 Elm St'),
        (3, 'Bob Johnson', '789 Oak St')
    ) AS Customer(c_custkey, c_name, c_address)
),
LineitemCTE AS (
    SELECT l_orderkey, l_extendedprice
    FROM (
        VALUES (1, 50.0),
        (1, 75.0),
        (2, 100.0),
        (3, 25.0),
        (4, 50.0)
    ) AS Lineitem(l_orderkey, l_extendedprice)
),
OrdersCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.0),
        (2, 1, 200.0),
        (3, 2, 50.0),
        (4, 2, 75.0),
        (5, 3, 150.0)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
)
SELECT s.o_orderkey, s.o_custkey, s.o_totalprice, c.c_name, c.c_address,
    SUM(s.o_totalprice) OVER (PARTITION BY s.o_custkey) AS TotalSales,
    AVG(s.o_totalprice) OVER (PARTITION BY s.o_custkey) AS AvgSales,
    MAX(s.o_totalprice) OVER (PARTITION BY s.o_custkey) AS MaxSales,
    MIN(s.o_totalprice) OVER (PARTITION BY s.o_custkey) AS MinSales
FROM SalesCTE s
INNER JOIN CustomerCTE c ON s.o_custkey = c.c_custkey
INNER JOIN (
    SELECT l_orderkey, l_extendedprice
    FROM (
        VALUES (1, 50.0),
        (1, 75.0),
        (2, 100.0),
        (3, 25.0),
        (4, 50.0)
    ) AS Lineitem(l_orderkey, l_extendedprice)
) l ON s.o_orderkey = l.l_orderkey
WHERE s.o_totalprice IN (
    SELECT o_totalprice
    FROM (
        SELECT o_orderkey, o_custkey, o_totalprice
        FROM (
            VALUES (1, 1, 100.0),
            (2, 1, 200.0),
            (3, 2, 50.0),
            (4, 2, 75.0),
            (5, 3, 150.0)
        ) AS Orders(o_orderkey, o_custkey, o_totalprice)
    ) o
    WHERE o.o_custkey = s.o_custkey
)
AND c.c_name LIKE '%Smith%'
AND CASE WHEN s.o_totalprice > 1000 THEN 'High' WHEN s.o_totalprice BETWEEN 500 AND 1000 THEN 'Medium' ELSE 'Low' END = 'High'
