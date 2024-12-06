-- tsql sql:
SELECT c.c_custkey, c.c_name, SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
FROM (
    VALUES (1, 'Customer 1', 100.00, 'Address 1', 'Phone 1', 'Comment 1', 1),
    (2, 'Customer 2', 200.00, 'Address 2', 'Phone 2', 'Comment 2', 2)
) AS c (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
LEFT JOIN (
    VALUES (1, 1, 1000.00),
    (2, 1, 2000.00)
) AS o (o_orderkey, o_custkey, o_totalprice)
ON c.c_custkey = o.o_custkey
LEFT JOIN (
    VALUES (1, 1000.00, 0.10),
    (2, 2000.00, 0.20)
) AS l (l_orderkey, l_extendedprice, l_discount)
ON o.o_orderkey = l.l_orderkey
LEFT JOIN (
    VALUES (1, 'Nation 1'),
    (2, 'Nation 2')
) AS n (n_nationkey, n_name)
ON c.c_nationkey = n.n_nationkey
WHERE c.c_acctbal > 0.00 AND l.l_orderkey IS NULL
GROUP BY c.c_custkey, c.c_name, c.c_acctbal, c.c_phone, n.n_name, c.c_address, c.c_comment
ORDER BY revenue DESC;
