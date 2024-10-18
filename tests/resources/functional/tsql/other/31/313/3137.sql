--Query type: DML
CREATE TABLE #MyTable
(
    CustomerID INT NOT NULL,
    SalesAmount DECIMAL(10, 2),
    ModifiedDate DATETIME
);

CREATE TABLE #AuditTable
(
    CustomerID INT NOT NULL,
    OldSalesAmount DECIMAL(10, 2),
    NewSalesAmount DECIMAL(10, 2),
    ModifiedDate DATETIME
);

INSERT INTO #MyTable
    (
        CustomerID,
        SalesAmount,
        ModifiedDate
    )
VALUES
    (
        1,
        100.00,
        '2022-01-01'
    ),
    (
        2,
        200.00,
        '2022-01-02'
    ),
    (
        3,
        300.00,
        '2022-01-03'
    ),
    (
        4,
        400.00,
        '2022-01-04'
    ),
    (
        5,
        500.00,
        '2022-01-05'
    ),
    (
        6,
        600.00,
        '2022-01-06'
    ),
    (
        7,
        700.00,
        '2022-01-07'
    ),
    (
        8,
        800.00,
        '2022-01-08'
    ),
    (
        9,
        900.00,
        '2022-01-09'
    ),
    (
        10,
        1000.00,
        '2022-01-10'
    );

UPDATE mt
SET SalesAmount = SalesAmount * 1.25
OUTPUT inserted.CustomerID, deleted.SalesAmount, inserted.SalesAmount, inserted.ModifiedDate
INTO #AuditTable
FROM #MyTable mt;

SELECT CustomerID, OldSalesAmount, NewSalesAmount, ModifiedDate
FROM #AuditTable;

SELECT CustomerID, SalesAmount, ModifiedDate
FROM #MyTable;

-- REMORPH CLEANUP: DROP TABLE #MyTable;
-- REMORPH CLEANUP: DROP TABLE #AuditTable;