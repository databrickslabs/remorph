--Query type: DML
CREATE TABLE #tempResult
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus CHAR(1),
    o_totalprice DECIMAL(10, 2)
);

INSERT INTO #tempResult
(
    o_orderkey,
    o_custkey,
    o_orderstatus,
    o_totalprice
)
VALUES
(
    1,
    1,
    'O',
    100.00
),
(
    2,
    2,
    'O',
    200.00
),
(
    3,
    3,
    'O',
    300.00
),
(
    4,
    4,
    'O',
    400.00
),
(
    5,
    5,
    'O',
    500.00
);

CREATE STATISTICS stats_o_totalprice
ON #tempResult (o_totalprice);

UPDATE STATISTICS #tempResult
WITH FULLSCAN;

WITH tempCTE AS
(
    SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice
    FROM #tempResult
)
SELECT *
FROM tempCTE;

SELECT *
FROM #tempResult;

-- REMORPH CLEANUP: DROP TABLE #tempResult;