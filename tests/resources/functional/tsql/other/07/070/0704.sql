-- tsql sql:
CREATE TABLE #target
(
    c_custkey INT,
    c_name VARCHAR(50),
    o_orderkey INT,
    o_orderdate DATE,
    o_totalprice DECIMAL(10, 2)
);

INSERT INTO #target
(
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
)
SELECT
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
FROM
(
    VALUES
    (
        1,
        'John Doe',
        1001,
        '2020-01-01',
        100.00
    ),
    (
        2,
        'Jane Doe',
        1002,
        '2020-01-15',
        200.00
    ),
    (
        3,
        'Bob Smith',
        1003,
        '2020-02-01',
        300.00
    )
) AS customers
(
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
);

CREATE TABLE #source
(
    c_custkey INT,
    c_name VARCHAR(50),
    o_orderkey INT,
    o_orderdate DATE,
    o_totalprice DECIMAL(10, 2)
);

INSERT INTO #source
(
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
)
SELECT
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
FROM
(
    VALUES
    (
        1,
        'John Doe',
        1001,
        '2020-01-01',
        150.00
    ),
    (
        2,
        'Jane Doe',
        1002,
        '2020-01-15',
        250.00
    ),
    (
        3,
        'Bob Smith',
        1003,
        '2020-02-01',
        350.00
    )
) AS customers
(
    c_custkey,
    c_name,
    o_orderkey,
    o_orderdate,
    o_totalprice
);

MERGE INTO #target AS t
USING #source AS s
ON t.c_custkey = s.c_custkey
WHEN MATCHED THEN
UPDATE SET t.o_totalprice = s.o_totalprice;

SELECT * FROM #target;
