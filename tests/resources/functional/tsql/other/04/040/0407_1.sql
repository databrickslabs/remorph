--Query type: DDL
CREATE TABLE #MyCTE ( ProductKey INT, OrderDateKey INT, Sales DECIMAL(10, 2) );
INSERT INTO #MyCTE
SELECT ProductKey, OrderDateKey, SUM(SalesAmount) AS Sales
FROM (
    VALUES (1, 1, 100.0),
           (1, 2, 200.0),
           (2, 1, 50.0),
           (2, 2, 75.0)
) AS T (ProductKey, OrderDateKey, SalesAmount)
GROUP BY ProductKey, OrderDateKey;
CREATE INDEX my_index ON #MyCTE ( ProductKey, OrderDateKey );
SELECT * FROM #MyCTE;
-- REMORPH CLEANUP: DROP TABLE #MyCTE;
