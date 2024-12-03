--Query type: DQL
WITH temp_result AS (
    SELECT p_partkey, AVG(ps_supplycost) AS AverageCost, SUM(ps_availqty) AS Total
    FROM (
        VALUES (1, 10.0, 100),
               (2, 20.0, 200),
               (3, 30.0, 300)
    ) AS ps (p_partkey, ps_supplycost, ps_availqty)
    GROUP BY p_partkey
    HAVING SUM(ps_availqty) > 500 AND AVG(ps_supplycost) < 25.0
)
SELECT p_partkey, AverageCost, Total
FROM temp_result
