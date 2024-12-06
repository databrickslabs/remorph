-- tsql sql:
CREATE TABLE #wages
(
    o_orderpriority TINYINT NULL,
    l_extendedprice DECIMAL NULL,
    ps_supplycost DECIMAL NULL,
    ps_availqty TINYINT NULL,
    o_totalprice DECIMAL NULL
);

INSERT INTO #wages
(
    o_orderpriority,
    l_extendedprice,
    ps_supplycost,
    ps_availqty,
    o_totalprice
)
VALUES
(
    1,
    10.00,
    NULL,
    NULL,
    NULL
),
(
    2,
    20.00,
    NULL,
    NULL,
    NULL
),
(
    3,
    30.00,
    NULL,
    NULL,
    NULL
),
(
    4,
    40.00,
    NULL,
    NULL,
    NULL
),
(
    5,
    NULL,
    10000.00,
    NULL,
    NULL
),
(
    6,
    NULL,
    20000.00,
    NULL,
    NULL
),
(
    7,
    NULL,
    30000.00,
    NULL,
    NULL
),
(
    8,
    NULL,
    40000.00,
    NULL,
    NULL
),
(
    9,
    NULL,
    NULL,
    15000,
    3
),
(
    10,
    NULL,
    NULL,
    25000,
    2
),
(
    11,
    NULL,
    NULL,
    20000,
    6
),
(
    12,
    NULL,
    NULL,
    14000,
    4
);

WITH wages AS
(
    SELECT CAST(COALESCE(o_orderpriority * 40 * 52, l_extendedprice, ps_supplycost * ps_availqty) AS DECIMAL(10,2)) AS TotalSalary
    FROM #wages
)
SELECT TotalSalary
FROM wages
ORDER BY TotalSalary
