--Query type: DDL
CREATE TABLE #SupplierWithMinCost
(
    s_suppkey INT,
    min_cost DECIMAL(10, 2)
);

INSERT INTO #SupplierWithMinCost (s_suppkey, min_cost)
SELECT s_suppkey, MIN(ps_supplycost) AS min_cost
FROM (
    VALUES (1, 100),
           (2, 200),
           (3, 50)
) AS ps (ps_suppkey, ps_supplycost)
INNER JOIN (
    VALUES (1, 'Supplier#1'),
           (2, 'Supplier#2'),
           (3, 'Supplier#3')
) AS s (s_suppkey, s_name)
ON ps.ps_suppkey = s.s_suppkey
GROUP BY s_suppkey
HAVING MIN(ps_supplycost) > 50;

CREATE NONCLUSTERED INDEX FISupplierWithMinCost
ON #SupplierWithMinCost (s_suppkey, min_cost);

SELECT * FROM #SupplierWithMinCost;
