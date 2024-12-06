-- tsql sql:
ALTER AUTHORIZATION ON OBJECT::CTE TO User1;

WITH CTE AS (
    SELECT
        T1.l_orderkey,
        T2.l_extendedprice,
        T3.ps_supplycost,
        T1.l_orderkey + T2.l_extendedprice + T3.ps_supplycost AS total,
        CASE
            WHEN T1.l_orderkey > 10000 THEN 'high'
            WHEN T1.l_orderkey < 5000 THEN 'low'
            ELSE 'medium'
        END AS category,
        ROW_NUMBER() OVER (PARTITION BY T1.l_orderkey ORDER BY T2.l_extendedprice) AS row_num,
        LAG(T2.l_extendedprice, 1, 0) OVER (PARTITION BY T1.l_orderkey ORDER BY T2.l_extendedprice) AS prev_extendedprice,
        LEAD(T2.l_extendedprice, 1, 0) OVER (PARTITION BY T1.l_orderkey ORDER BY T2.l_extendedprice) AS next_extendedprice,
        SUM(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS sum_supplycost,
        AVG(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS avg_supplycost,
        MAX(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS max_supplycost,
        MIN(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS min_supplycost,
        COUNT(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS count_supplycost,
        STDEV(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS stdev_supplycost,
        VAR(T3.ps_supplycost) OVER (PARTITION BY T1.l_orderkey) AS var_supplycost
    FROM
        (VALUES (1, 10000), (2, 20000), (3, 30000)) AS T1(l_orderkey, l_discount),
        (VALUES (1, 100000), (2, 200000), (3, 300000)) AS T2(l_orderkey, l_extendedprice),
        (VALUES (1, 1000000), (2, 2000000), (3, 3000000)) AS T3(ps_partkey, ps_supplycost)
    WHERE
        T1.l_orderkey = T2.l_orderkey AND T2.l_orderkey = T3.ps_partkey
)

SELECT * FROM CTE
ORDER BY l_orderkey, l_extendedprice, ps_supplycost
