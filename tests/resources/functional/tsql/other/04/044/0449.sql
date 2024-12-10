-- tsql sql:
SELECT *
INTO #orders
FROM (
    VALUES (1, 2),
           (3, 4)
) AS orders (
    o_orderkey,
    o_custkey
);

CREATE CLUSTERED INDEX idx_orders
ON #orders (
    o_orderkey,
    o_custkey
);

SELECT *
FROM #orders;
-- REMORPH CLEANUP: DROP TABLE #orders;
