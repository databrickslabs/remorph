-- tsql sql:
WITH temp_result AS (
    SELECT c_custkey, c_name, n_name
    FROM (
        VALUES (1, 'Customer1', 'USA'),
               (2, 'Customer2', 'Canada')
    ) AS customer(c_custkey, c_name, c_nationkey)
    CROSS JOIN (
        VALUES ('USA', 1),
               ('Canada', 2)
    ) AS nation(n_name, n_nationkey)
    WHERE customer.c_nationkey = nation.n_nationkey
),
orders AS (
    SELECT o_custkey, o_totalprice
    FROM (
        VALUES (1, 1000.0),
               (2, 2000.0)
    ) AS orders(o_custkey, o_totalprice)
)
SELECT tr.c_name, tr.n_name, SUM(o.o_totalprice) AS total
FROM temp_result tr
JOIN orders o ON tr.c_custkey = o.o_custkey
WHERE tr.n_name = 'USA'
GROUP BY tr.c_name, tr.n_name
HAVING SUM(o.o_totalprice) > 1000
ORDER BY total DESC;
