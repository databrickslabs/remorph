-- tsql sql:
CREATE TABLE #ext_orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus VARCHAR(10),
    o_totalprice DECIMAL(10, 2),
    o_orderdate DATE,
    o_orderpriority VARCHAR(15),
    o_clerk VARCHAR(15),
    o_shippriority INT,
    o_comment VARCHAR(79)
);

INSERT INTO #ext_orders
(
    o_orderkey,
    o_custkey,
    o_orderstatus,
    o_totalprice,
    o_orderdate,
    o_orderpriority,
    o_clerk,
    o_shippriority,
    o_comment
)
VALUES
(
    1,
    1,
    'Status1',
    100.00,
    '2022-01-01',
    'Priority1',
    'Clerk1',
    1,
    'Comment1'
),
(
    2,
    2,
    'Status2',
    200.00,
    '2022-01-02',
    'Priority2',
    'Clerk2',
    2,
    'Comment2'
);

DELETE FROM #ext_orders
WHERE o_orderkey IN (1, 2);

SELECT *
FROM #ext_orders;
-- REMORPH CLEANUP: DROP TABLE #ext_orders;
