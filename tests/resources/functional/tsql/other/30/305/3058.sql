--Query type: DML
WITH SalesCTE AS (
    SELECT ProductKey, UnitPrice
    FROM (
        VALUES (100, 20.00),
               (150, 30.00),
               (200, 40.00)
    ) AS Sales(ProductKey, UnitPrice)
)
SELECT ProductKey, UnitPrice
INTO #Sales
FROM SalesCTE;

UPDATE #Sales WITH (ROWLOCK)
SET UnitPrice = 50
WHERE ProductKey = 150;

SELECT *
FROM #Sales;

-- REMORPH CLEANUP: DROP TABLE #Sales;
