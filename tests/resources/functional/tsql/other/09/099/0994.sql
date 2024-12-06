-- tsql sql:
CREATE TABLE #file_content (CONTENT VARBINARY(MAX));
INSERT INTO #file_content (CONTENT)
SELECT * FROM OPENROWSET(BULK 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\pythonAnalytics.zip', SINGLE_BLOB) AS file_content;
SELECT CONTENT FROM (VALUES((SELECT CONTENT FROM #file_content))) AS ExternalLibrary(CONTENT);
SELECT * FROM #file_content;
-- REMORPH CLEANUP: DROP TABLE #file_content;
