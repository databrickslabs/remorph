-- tsql sql:
CREATE TABLE #CustomerCTE (CustomerName VARCHAR(50), CustomerID INT);
INSERT INTO #CustomerCTE (CustomerName, CustomerID)
VALUES ('Customer1', 100), ('Customer2', 200);
CREATE STATISTICS CustomerStats2 ON #CustomerCTE (CustomerID);
DROP STATISTICS #CustomerCTE.CustomerStats2;
SELECT * FROM #CustomerCTE;
-- REMORPH CLEANUP: DROP TABLE #CustomerCTE;
