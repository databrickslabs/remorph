--Query type: DDL
CREATE TABLE #CustomerOrders
(
    c_custkey INT,
    o_orderdate DATE
);

INSERT INTO #CustomerOrders (c_custkey, o_orderdate)
VALUES
    (1, '2020-01-01'),
    (2, '2020-01-02'),
    (3, '2020-01-03');

CREATE STATISTICS CustomerOrder ON #CustomerOrders (c_custkey, o_orderdate)
WITH FULLSCAN, PERSIST_SAMPLE_PERCENT = ON;

SELECT *
FROM #CustomerOrders;

-- REMORPH CLEANUP: DROP TABLE #CustomerOrders;
-- REMORPH CLEANUP: DROP STATISTICS #CustomerOrders.CustomerOrder;