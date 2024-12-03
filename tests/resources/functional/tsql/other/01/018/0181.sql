--Query type: DDL
CREATE TABLE #orders_temp (o_orderkey INT, o_orderdate DATE, o_totalprice DECIMAL(10, 2));
WITH orders_cte AS (
    SELECT o_orderkey, o_orderdate, o_totalprice
    FROM orders
)
INSERT INTO #orders_temp
SELECT *
FROM orders_cte;
CREATE CLUSTERED INDEX idx_orders_temp ON #orders_temp (o_orderdate, o_orderkey);
SELECT * FROM #orders_temp;
-- REMORPH CLEANUP: DROP TABLE #orders_temp;
