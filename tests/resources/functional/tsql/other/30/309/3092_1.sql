-- tsql sql:
CREATE TABLE #ZeroSales
(
    DeletedOrderID INT,
    RemovedOnDate DATETIME
);

INSERT INTO #ZeroSales
(
    DeletedOrderID,
    RemovedOnDate
)
SELECT *
FROM (
    VALUES
    (
        1,
        '2023-01-01'
    ),
    (
        2,
        '2023-01-02'
    )
) AS temp
(
    DeletedOrderID,
    RemovedOnDate
);

SELECT *
FROM #ZeroSales;
-- REMORPH CLEANUP: DROP TABLE #ZeroSales;
