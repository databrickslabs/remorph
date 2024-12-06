-- tsql sql:
WITH SalesCTE AS (
    SELECT
        o_orderkey,
        o_custkey,
        o_orderstatus,
        o_totalprice,
        o_orderdate,
        ROW_NUMBER() OVER (PARTITION BY o_custkey ORDER BY o_orderdate) AS RowNum,
        RANK() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS Rank,
        DENSE_RANK() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS DenseRank,
        SUM(o_totalprice) OVER (PARTITION BY o_custkey) AS TotalSales,
        AVG(o_totalprice) OVER (PARTITION BY o_custkey) AS AvgSales,
        MAX(o_totalprice) OVER (PARTITION BY o_custkey) AS MaxSales,
        MIN(o_totalprice) OVER (PARTITION BY o_custkey) AS MinSales
    FROM (
        VALUES
            (1, 1, 'O', 100.00, '2020-01-01'),
            (2, 1, 'O', 200.00, '2020-01-15'),
            (3, 2, 'O', 50.00, '2020-02-01'),
            (4, 2, 'O', 75.00, '2020-03-01'),
            (5, 3, 'O', 150.00, '2020-04-01')
    ) AS Orders(o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate)
),
CustomerCTE AS (
    SELECT
        c_custkey,
        c_name,
        c_address,
        c_phone,
        c_acctbal
    FROM (
        VALUES
            (1, 'John Doe', '123 Main St', '123-456-7890', 1000.00),
            (2, 'Jane Doe', '456 Elm St', '987-654-3210', 500.00),
            (3, 'Bob Smith', '789 Oak St', '555-123-4567', 2000.00)
    ) AS Customer(c_custkey, c_name, c_address, c_phone, c_acctbal)
)
SELECT TOP 10
    s.o_orderkey,
    s.o_custkey,
    s.o_orderstatus,
    s.o_totalprice,
    s.o_orderdate,
    c.c_name,
    c.c_address,
    c.c_phone,
    c.c_acctbal,
    s.TotalSales,
    s.AvgSales,
    s.MaxSales,
    s.MinSales
FROM
    SalesCTE s
    INNER JOIN CustomerCTE c ON s.o_custkey = c.c_custkey
WHERE
    s.o_orderstatus = 'O'
    AND s.TotalSales > 10000
ORDER BY
    s.o_totalprice DESC;
