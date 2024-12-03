--Query type: DDL
CREATE TABLE #orders_local_temporary
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus CHAR(1),
    o_totalprice DECIMAL(10, 2),
    o_orderdate DATE,
    o_orderpriority CHAR(5),
    o_clerk CHAR(10),
    o_shippriority INT,
    o_comment VARCHAR(100)
);

WITH orders_cte AS
(
    SELECT *
    FROM (
        VALUES (1, 1, 'O', 100.00, '2020-01-01', 'HIGH', 'Clerk1', 1, 'Comment1')
    ) AS orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment)
)
INSERT INTO #orders_local_temporary
SELECT *
FROM orders_cte;

SELECT *
FROM #orders_local_temporary;
-- REMORPH CLEANUP: DROP TABLE #orders_local_temporary;
