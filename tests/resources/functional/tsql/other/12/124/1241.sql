--Query type: DDL
CREATE TABLE #Test.Customer
(
    C_CUSTKEY INT PRIMARY KEY,
    C_NAME VARCHAR(25),
    C_ADDRESS VARCHAR(25),
    C_NATIONKEY INT,
    C_PHONE VARCHAR(25),
    C_ACCTBAL DECIMAL(10, 2),
    C_MKTSEGMENT VARCHAR(25),
    C_COMMENT VARCHAR(100)
);

INSERT INTO #Test.Customer
(
    C_CUSTKEY,
    C_NAME,
    C_ADDRESS,
    C_NATIONKEY,
    C_PHONE,
    C_ACCTBAL,
    C_MKTSEGMENT,
    C_COMMENT
)
SELECT
    C_CUSTKEY,
    C_NAME,
    C_ADDRESS,
    C_NATIONKEY,
    C_PHONE,
    C_ACCTBAL,
    C_MKTSEGMENT,
    C_COMMENT
FROM
(
    VALUES
    (
        1,
        'Name1',
        'Address1',
        1,
        'Phone1',
        100.00,
        'Segment1',
        'Comment1'
    )
) AS temp_result
(
    C_CUSTKEY,
    C_NAME,
    C_ADDRESS,
    C_NATIONKEY,
    C_PHONE,
    C_ACCTBAL,
    C_MKTSEGMENT,
    C_COMMENT
);
