-- tsql sql:
CREATE TABLE temp_table (l_discount DECIMAL(5,2), l_extendedprice INT, l_linenumber INT, l_quantity INT, l_orderkey INT, l_shipmode VARCHAR(1));

SELECT *
INTO #temp
FROM (
    VALUES (0.01, 100, 1000, 10000, 1, 'a'),
           (0.05, 200, 2000, 20000, 2, 'b'),
           (0.10, 300, 3000, 30000, 3, 'c')
) AS temp (l_discount, l_extendedprice, l_linenumber, l_quantity, l_orderkey, l_shipmode);

SELECT
    CASE
        WHEN l_discount = 0.01 THEN 'Low'
        WHEN l_discount = 0.05 THEN 'Medium'
        ELSE 'High'
    END AS discount_level,
    SUM(l_extendedprice) AS total_revenue,
    AVG(l_extendedprice * (1 - l_discount)) AS average_revenue,
    MAX(l_extendedprice) AS max_revenue,
    MIN(l_extendedprice) AS min_revenue,
    COUNT(l_orderkey) AS num_orders,
    GROUPING(l_shipmode) AS grouping
FROM #temp
GROUP BY ROLLUP(l_discount, l_shipmode)
HAVING SUM(l_extendedprice) > 200
ORDER BY discount_level;
