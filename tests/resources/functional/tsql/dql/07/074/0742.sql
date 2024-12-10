-- tsql sql:
WITH ranked_lineitem AS (
    SELECT l_orderkey, l_extendedprice, ROW_NUMBER() OVER (PARTITION BY l_orderkey ORDER BY l_extendedprice) AS row_num
    FROM (
        VALUES (1, 10.0),
               (1, 11.0),
               (1, 12.0),
               (2, 20.0),
               (2, 21.0),
               (2, 22.0)
    ) AS lineitem(l_orderkey, l_extendedprice)
)
SELECT l_orderkey, l_extendedprice, (
    SELECT l_extendedprice
    FROM ranked_lineitem rl2
    WHERE rl2.l_orderkey = rl1.l_orderkey AND rl2.row_num = 2
) AS l_extendedprice_2nd
FROM ranked_lineitem rl1;
