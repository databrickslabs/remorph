-- tsql sql:
CREATE TABLE #customer_sales
(
    c_custkey INT,
    c_nationkey INT,
    total_sales DECIMAL(10, 2)
);

INSERT INTO #customer_sales (c_custkey, c_nationkey, total_sales)
SELECT c_custkey, c_nationkey, SUM(EXTENDEDPRICE * (1 - DISCOUNT)) AS total_sales
FROM (
    VALUES (1, 1, 100.0, 0.1),
           (2, 2, 200.0, 0.2),
           (3, 3, 300.0, 0.3)
) AS sales (c_custkey, c_nationkey, EXTENDEDPRICE, DISCOUNT)
GROUP BY c_custkey, c_nationkey;

CREATE NONCLUSTERED INDEX idx_customer_sales
ON #customer_sales (c_custkey, c_nationkey);

ALTER INDEX idx_customer_sales
ON #customer_sales
REBUILD PARTITION = ALL
WITH (DATA_COMPRESSION = NONE);

SELECT *
FROM #customer_sales;

-- REMORPH CLEANUP: DROP INDEX idx_customer_sales ON #customer_sales;
-- REMORPH CLEANUP: DROP TABLE #customer_sales;
