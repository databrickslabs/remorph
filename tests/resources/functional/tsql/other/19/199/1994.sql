-- tsql sql:
CREATE TABLE #temp_result (ProductID VARCHAR(10), ProductName VARCHAR(100));
INSERT INTO #temp_result (ProductID, ProductName)
VALUES ('1', 'Product1'), ('2', 'Product2');
CREATE INDEX idx_temp_result_ProductID ON #temp_result (ProductID);
DROP INDEX idx_temp_result_ProductID ON #temp_result;
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
