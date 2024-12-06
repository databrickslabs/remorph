-- tsql sql:
SELECT c.c_custkey, c.c_name, SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
FROM (
    VALUES (1, 'Customer1', 100.0, '123 Main St', '123-456-7890', 'Comment1', 1),
    (2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 2)
) c (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
INNER JOIN (
    VALUES (1, 1, 100.0),
    (2, 2, 200.0)
) o (o_orderkey, o_custkey, o_totalprice)
ON c.c_custkey = o.o_custkey
INNER JOIN (
    VALUES (1, 1, 10.0, 'R'),
    (2, 2, 20.0, 'R')
) l (l_orderkey, l_extendedprice, l_discount, l_returnflag)
ON o.o_orderkey = l.l_orderkey
INNER JOIN (
    VALUES (1, 'USA'),
    (2, 'Canada')
) n (n_nationkey, n_name)
ON c.c_nationkey = n.n_nationkey
WHERE l.l_returnflag = 'R'
GROUP BY c.c_custkey, c.c_name, c.c_acctbal, c.c_phone, n.n_name, c.c_address, c.c_comment
ORDER BY revenue DESC;
