--Query type: DML
CREATE TABLE #SalesOrder
(
    OrderID INT,
    CustomerID INT,
    OrderDate DATE,
    TotalCost DECIMAL(10, 2)
)
ON [PRIMARY];

INSERT INTO #SalesOrder
(
    OrderID,
    CustomerID,
    OrderDate,
    TotalCost
)
VALUES
(
    1,
    1,
    '2020-01-01',
    100.00
),
(
    1001,
    2,
    '2020-01-02',
    200.00
),
(
    2001,
    3,
    '2020-01-03',
    300.00
),
(
    3001,
    4,
    '2020-01-04',
    400.00
),
(
    4001,
    5,
    '2020-01-05',
    500.00
),
(
    5001,
    6,
    '2020-01-06',
    600.00
);

ALTER TABLE #SalesOrder
REBUILD PARTITION = ALL
WITH (DATA_COMPRESSION = PAGE ON PARTITIONS (1 TO 6));

SELECT *
FROM #SalesOrder;

-- REMORPH CLEANUP: DROP TABLE #SalesOrder;
