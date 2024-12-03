--Query type: DQL
WITH temp_result AS (
    SELECT c_custkey, o_orderkey, l_extendedprice
    FROM (
        VALUES (1, 1, 10.0),
               (1, 2, 20.0),
               (2, 3, 30.0),
               (2, 4, 40.0),
               (3, 5, 50.0),
               (3, 6, 60.0)
    ) AS temp_table (c_custkey, o_orderkey, l_extendedprice)
)
SELECT c_custkey, o_orderkey, l_extendedprice,
       COUNT(l_extendedprice) OVER (PARTITION BY c_custkey ORDER BY o_orderkey) AS count_l_extendedprice_Range_Pre,
       SUM(l_extendedprice) OVER (PARTITION BY c_custkey ORDER BY o_orderkey) AS sum_l_extendedprice_Range_Pre,
       AVG(l_extendedprice) OVER (PARTITION BY c_custkey ORDER BY o_orderkey) AS avg_l_extendedprice_Range_Pre,
       MIN(l_extendedprice) OVER (PARTITION BY c_custkey ORDER BY o_orderkey) AS min_l_extendedprice_Range_Pre,
       MAX(l_extendedprice) OVER (PARTITION BY c_custkey ORDER BY o_orderkey) AS max_l_extendedprice_Range_Pre
FROM temp_result
ORDER BY c_custkey, o_orderkey;
