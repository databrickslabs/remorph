-- tsql sql:
CREATE TABLE #Orders
(
    ORDERKEY INT,
    ORDERDATE DATE,
    TOTALPRICE DECIMAL(10, 2)
);

INSERT INTO #Orders
(
    ORDERKEY,
    ORDERDATE,
    TOTALPRICE
)
SELECT *
FROM (
    VALUES
    (
        1,
        '2020-01-01',
        100.00
    ),
    (
        2,
        '2020-01-02',
        200.00
    ),
    (
        3,
        '2020-01-03',
        300.00
    )
) AS Orders
(
    ORDERKEY,
    ORDERDATE,
    TOTALPRICE
);

SELECT *
FROM #Orders;
-- REMORPH CLEANUP: DROP TABLE #Orders;
