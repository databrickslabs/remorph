--Query type: DCL
WITH customer AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, '123 Main St', '123-456-7890', 'Comment1', 1),
            (2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS c (custkey, name, acctbal, address, phone, comment, nationkey)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, '2020-01-01'),
            (2, 1, '2020-01-15'),
            (3, 2, '2020-02-01')
    ) AS o (orderkey, custkey, orderdate)
),
lineitem AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 10.00, 0.1),
            (2, 1, 20.00, 0.2),
            (3, 2, 30.00, 0.3)
    ) AS l (orderkey, linenumber, extendedprice, discount)
),
nation AS (
    SELECT *
    FROM (
        VALUES
            (1, 'USA'),
            (2, 'Canada')
    ) AS n (nationkey, nation)
),
customer_orders AS (
    SELECT c.custkey, COUNT(o.orderkey) AS order_count
    FROM customer c
    INNER JOIN orders o ON c.custkey = o.custkey
    GROUP BY c.custkey
)
SELECT c.custkey, c.name, SUM(l.extendedprice * (1 - l.discount)) AS revenue, c.acctbal, n.nation, c.address, c.phone, c.comment
FROM customer c
INNER JOIN customer_orders co ON c.custkey = co.custkey
INNER JOIN orders o ON c.custkey = o.custkey
INNER JOIN lineitem l ON o.orderkey = l.orderkey
INNER JOIN nation n ON c.nationkey = n.nationkey
WHERE c.acctbal > 0.00 AND co.order_count > 1
GROUP BY c.custkey, c.name, c.acctbal, c.address, c.phone, c.comment, n.nation
ORDER BY revenue DESC;
