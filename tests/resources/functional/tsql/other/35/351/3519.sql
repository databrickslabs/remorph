--Query type: DCL
WITH Customers AS (
    SELECT c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey
    FROM (
        VALUES 
            (1, 'Customer1', 100.0, '123 Main St', '123-456-7890', 'Comment1', 1),
            (2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS c (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
),
Orders AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES 
            (1, 1, 100.0),
            (2, 2, 200.0)
    ) AS o (o_orderkey, o_custkey, o_totalprice)
),
LineItems AS (
    SELECT l_orderkey, l_extendedprice, l_discount, l_returnflag
    FROM (
        VALUES 
            (1, 1, 10.0, 'R'),
            (2, 2, 20.0, 'R')
    ) AS l (l_orderkey, l_extendedprice, l_discount, l_returnflag)
),
Nations AS (
    SELECT n_nationkey, n_name
    FROM (
        VALUES 
            (1, 'USA'),
            (2, 'Canada')
    ) AS n (n_nationkey, n_name)
)
SELECT 
    c.c_custkey, 
    c.c_name, 
    SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue,
    c.c_acctbal, 
    n.n_name, 
    c.c_address, 
    c.c_phone, 
    c.c_comment
FROM Customers c
INNER JOIN Orders o ON c.c_custkey = o.o_custkey
INNER JOIN LineItems l ON o.o_orderkey = l.l_orderkey
INNER JOIN Nations n ON c.c_nationkey = n.n_nationkey
WHERE l.l_returnflag = 'R'
GROUP BY 
    c.c_custkey, 
    c.c_name, 
    c.c_acctbal, 
    c.c_phone, 
    n.n_name, 
    c.c_address, 
    c.c_comment
ORDER BY revenue DESC;