--Query type: DDL
SELECT *
INTO #NewOrderTable
FROM (
    VALUES (
        1, '2020-01-01', 100.0
    ), (
        2, '2020-01-02', 200.0
    ), (
        3, '2020-01-03', 300.0
    )
) AS OrderData (
    OrderKey, OrderDate, TotalAmount
);

SELECT *
FROM #NewOrderTable;

-- REMORPH CLEANUP: DROP TABLE #NewOrderTable;
