--Query type: DDL
WITH CustomerOrdersCTE AS (
    SELECT c_custkey, c_name, o_orderkey, o_orderdate
    FROM (
        VALUES
            (1, 'Customer#001', 1, '1992-01-01'),
            (2, 'Customer#002', 2, '1992-01-02'),
            (3, 'Customer#003', 3, '1992-01-03')
    ) AS CustomerOrders (c_custkey, c_name, o_orderkey, o_orderdate)
)
SELECT *
FROM CustomerOrdersCTE
WHERE o_orderdate < '1992-12-31';