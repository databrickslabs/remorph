-- tsql sql:
SELECT c.custkey, c.name, SUM(o.totalprice) AS total
FROM (
    SELECT *
    FROM (
        VALUES (1, 'Customer1', 1),
               (2, 'Customer2', 2)
    ) AS customer (custkey, name, nationkey)
) c
INNER JOIN (
    SELECT *
    FROM (
        VALUES (1, 1, 1000.0),
               (2, 1, 2000.0),
               (3, 2, 500.0)
    ) AS orders (orderkey, custkey, totalprice)
) o
ON c.custkey = o.custkey
WHERE c.nationkey = 1
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 1000000
ORDER BY total DESC;
