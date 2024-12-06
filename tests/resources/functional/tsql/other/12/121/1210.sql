-- tsql sql:
CREATE TABLE Customer_Dim
(
    CUSTKEY INT PRIMARY KEY,
    NAME VARCHAR(50),
    ADDRESS VARCHAR(100),
    NATIONKEY INT,
    PHONE VARCHAR(20),
    ACCTBAL DECIMAL(10, 2),
    MKTSEGMENT VARCHAR(50),
    COMMENT VARCHAR(100)
);

INSERT INTO Customer_Dim
(
    CUSTKEY,
    NAME,
    ADDRESS,
    NATIONKEY,
    PHONE,
    ACCTBAL,
    MKTSEGMENT,
    COMMENT
)
SELECT
    CUSTKEY,
    NAME,
    ADDRESS,
    NATIONKEY,
    PHONE,
    ACCTBAL,
    MKTSEGMENT,
    COMMENT
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
    ),
    (
        2,
        'Name2',
        'Address2',
        2,
        'Phone2',
        200.00,
        'Segment2',
        'Comment2'
    )
) AS temp_result
(
    CUSTKEY,
    NAME,
    ADDRESS,
    NATIONKEY,
    PHONE,
    ACCTBAL,
    MKTSEGMENT,
    COMMENT
);

SELECT * FROM Customer_Dim;
-- REMORPH CLEANUP: DROP TABLE Customer_Dim;
