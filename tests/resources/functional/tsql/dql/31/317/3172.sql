--Query type: DQL
SELECT p_partkey, Total = SUM(ps_supplycost * ps_availqty)
FROM (
    VALUES
        (1, 100, 1000.0),
        (2, 200, 2000.0),
        (3, 300, 3000.0),
        (4, 400, 4000.0),
        (5, 500, 5000.0)
) AS t (p_partkey, ps_supplycost, ps_availqty)
GROUP BY p_partkey
HAVING SUM(ps_supplycost * ps_availqty) > 1000000.00;