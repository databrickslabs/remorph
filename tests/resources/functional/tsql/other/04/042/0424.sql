-- tsql sql:
CREATE TABLE #TempData (CUSTKEY INT, NAME VARCHAR(50), ACCTBAL DECIMAL(10, 2), TotalOrders INT);
INSERT INTO #TempData (CUSTKEY, NAME, ACCTBAL, TotalOrders)
VALUES (1, 'John', 100.0, 2);
CREATE INDEX idx_custkey ON #TempData (CUSTKEY);
SELECT 'DROP INDEX idx_custkey ON #TempData;' AS QueryToDropIndex;
-- REMORPH CLEANUP: DROP TABLE #TempData;
