--Query type: DQL
WITH SalesData AS (
    SELECT o_orderkey, o_custkey, o_totalprice, o_orderdate
    FROM (
        VALUES
            (1, 101, 1000.00, '2020-01-01'),
            (2, 102, 2000.00, '2020-01-15'),
            (3, 103, 3000.00, '2020-02-01')
    ) AS TempTable (o_orderkey, o_custkey, o_totalprice, o_orderdate)
)
SELECT o_orderkey, o_custkey, o_totalprice, o_orderdate
FROM SalesData;
