-- tsql sql:
SELECT c.custkey, c.name, SUM(o.totalprice) AS total_revenue
FROM (
    VALUES (1, 'Customer1', 1),
           (2, 'Customer2', 2)
) AS c (custkey, name, nationkey)
JOIN (
    VALUES (1, 1, '1995-01-01', 1000.00),
           (2, 1, '1995-01-02', 2000.00)
) AS o (orderkey, custkey, orderdate, totalprice)
    ON c.custkey = o.custkey
WHERE c.nationkey = 1
    AND o.orderdate >= '1995-01-01'
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 1000000
ORDER BY total_revenue DESC;
