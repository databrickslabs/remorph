--Query type: DDL
CREATE TABLE #FactInternetSales3
(
    ProductKey INT NOT NULL,
    OrderDateKey INT NOT NULL,
    DueDateKey INT NOT NULL,
    ShipDateKey INT NOT NULL
);

WITH temp_result AS
(
    SELECT ProductKey, OrderDateKey, DueDateKey, ShipDateKey
    FROM (
        VALUES (1, 2, 3, 4),
               (5, 6, 7, 8)
    ) AS t (ProductKey, OrderDateKey, DueDateKey, ShipDateKey)
)
INSERT INTO #FactInternetSales3
SELECT ProductKey, OrderDateKey, DueDateKey, ShipDateKey
FROM temp_result;

SELECT *
FROM #FactInternetSales3;
-- REMORPH CLEANUP: DROP TABLE #FactInternetSales3;