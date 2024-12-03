--Query type: DDL
WITH customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, 'USA', '123 Main St', '123-456-7890', 'Comment1'),
            (2, 'Customer2', 200.00, 'Canada', '456 Elm St', '987-654-3210', 'Comment2')
    ) AS t1 (custkey, name, acctbal, nation, address, phone, comment)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 100.00),
            (2, 2, 200.00)
    ) AS t2 (orderkey, custkey, totalprice)
),
orderdetails AS (
    SELECT *
    FROM (
        VALUES
            (1, 10.00, 0.1, 'R'),
            (2, 20.00, 0.2, 'R')
    ) AS t3 (orderkey, extendedprice, discount, returnflag)
)
-- Main query
SELECT
    c.custkey,
    c.name,
    SUM(od.extendedprice * (1 - od.discount)) AS revenue,
    c.acctbal,
    c.nation,
    c.address,
    c.phone,
    c.comment
FROM customers c
INNER JOIN orders o ON c.custkey = o.custkey
INNER JOIN orderdetails od ON o.orderkey = od.orderkey
WHERE c.acctbal > 0.00 AND od.returnflag = 'R'
GROUP BY
    c.custkey,
    c.name,
    c.acctbal,
    c.address,
    c.phone,
    c.comment,
    c.nation
ORDER BY revenue DESC;
