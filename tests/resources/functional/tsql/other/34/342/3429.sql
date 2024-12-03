--Query type: DML
CREATE TABLE #Lineitem
(
    L_Orderkey INT,
    L_Partkey INT,
    L_Suppkey INT,
    L_Linenumber INT,
    L_Quantity DECIMAL(10, 2),
    L_Extendedprice DECIMAL(10, 2),
    L_Discount DECIMAL(10, 2),
    L_Tax DECIMAL(10, 2),
    L_Returnflag CHAR(1),
    L_Linestatus CHAR(1),
    L_Shipdate DATE,
    L_Commitdate DATE,
    L_Recvdate DATE,
    L_Shipinstruct VARCHAR(25),
    L_Shipmode VARCHAR(10),
    L_Comment VARCHAR(44)
);

INSERT INTO #Lineitem
(
    L_Orderkey,
    L_Partkey,
    L_Suppkey,
    L_Linenumber,
    L_Quantity,
    L_Extendedprice,
    L_Discount,
    L_Tax,
    L_Returnflag,
    L_Linestatus,
    L_Shipdate,
    L_Commitdate,
    L_Recvdate,
    L_Shipinstruct,
    L_Shipmode,
    L_Comment
)
VALUES
(
    1,
    1,
    1,
    1,
    1.00,
    1.00,
    0.00,
    0.00,
    'R',
    'O',
    '1996-03-13',
    '1996-02-12',
    '1996-03-22',
    'TAKE BACK RETURN',
    'TRUCK',
    'blithely regular courts above the'
),
(
    2,
    2,
    2,
    2,
    2.00,
    2.00,
    0.00,
    0.00,
    'R',
    'O',
    '1996-03-13',
    '1996-02-12',
    '1996-03-22',
    'TAKE BACK RETURN',
    'TRUCK',
    'blithely regular courts above the'
);

WITH TotalQuantityCTE AS
(
    SELECT L_Partkey, SUM(L_Quantity) AS TotalQuantity
    FROM #Lineitem
    GROUP BY L_Partkey
    UNION ALL
    SELECT P_Partkey, 0 AS TotalQuantity
    FROM (
        VALUES (
            1,
            'part1',
            'mfgr1',
            'brand1',
            'type1',
            1,
            'container1',
            1.00,
            'comment1'
        ),
        (
            2,
            'part2',
            'mfgr2',
            'brand2',
            'type2',
            2,
            'container2',
            2.00,
            'comment2'
        )
    ) AS Part (
        P_Partkey,
        P_Name,
        P_Mfgr,
        P_Brand,
        P_Type,
        P_Size,
        P_Container,
        P_Retailprice,
        P_Comment
    )
    WHERE P_Partkey NOT IN (
        SELECT L_Partkey
        FROM #Lineitem
    )
)
UPDATE l
SET L_Quantity = L_Quantity * 2
FROM #Lineitem AS l
JOIN TotalQuantityCTE AS tq ON l.L_Partkey = tq.L_Partkey
WHERE tq.TotalQuantity > 1;

SELECT *
FROM #Lineitem;
-- REMORPH CLEANUP: DROP TABLE #Lineitem;
