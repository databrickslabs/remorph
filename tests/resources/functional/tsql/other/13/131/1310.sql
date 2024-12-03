--Query type: DDL
CREATE TABLE #t_orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus CHAR(1),
    o_totalprice DECIMAL(10, 2),
    o_orderdate DATE,
    o_orderpriority CHAR(4),
    o_clerk CHAR(4),
    o_shippriority INT,
    o_comment CHAR(7)
);

INSERT INTO #t_orders
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
SELECT *
FROM (
    VALUES
    (
        1,
        1,
        'A',
        100.00,
        '2020-01-01',
        'High',
        'John',
        1,
        'Comment'
    )
) AS tmp
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
);

SELECT *
FROM #t_orders;
-- REMORPH CLEANUP: DROP TABLE #t_orders;
