--Query type: DQL
SELECT p_partkey, SUM(ps_supplycost) AS Total
FROM (
    VALUES
        (1, 100.0),
        (2, 200.0),
        (3, 300.0),
        (4, 400.0),
        (5, 500.0),
        (6, 600.0),
        (7, 700.0),
        (8, 800.0),
        (9, 900.0),
        (10, 1000.0)
) AS t (p_partkey, ps_supplycost)
GROUP BY p_partkey
HAVING COUNT(*) > 0
