-- tsql sql:
DECLARE @MyTableVar TABLE (SummaryBefore NVARCHAR(max), SummaryAfter NVARCHAR(max));
CREATE TABLE #temp (DocumentSummary NVARCHAR(max), c_name NVARCHAR(max));
INSERT INTO #temp (DocumentSummary, c_name) VALUES (CAST('features' AS NVARCHAR(max)), 'Customer#000000001');
UPDATE t
SET DocumentSummary = STUFF(DocumentSummary, 28, 10, 'features')
OUTPUT DELETED.DocumentSummary AS SummaryBefore, INSERTED.DocumentSummary AS SummaryAfter
INTO @MyTableVar
FROM #temp t
WHERE c_name = 'Customer#000000001';
SELECT SummaryBefore, SummaryAfter FROM @MyTableVar;
-- REMORPH CLEANUP: DROP TABLE #temp;
-- REMORPH CLEANUP: DROP TABLE @MyTableVar;
