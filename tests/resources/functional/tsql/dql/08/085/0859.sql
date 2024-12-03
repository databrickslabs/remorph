--Query type: DQL
WITH lineitem AS (
    SELECT l_orderkey, l_discount, l_extendedprice
    FROM (
        VALUES
            (1, 0.1, 100.0),
            (2, 0.2, 200.0),
            (3, 0.3, 300.0)
    ) AS lineitem (l_orderkey, l_discount, l_extendedprice)
)
SELECT l_discount AS discount, l_extendedprice AS extendedprice
FROM lineitem;
