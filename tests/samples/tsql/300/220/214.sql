DROP TABLE IF EXISTS #SampleTempTable;
GO
CREATE TABLE #SampleTempTable (id INT, message nvarchar(50));
INSERT INTO #SampleTempTable VALUES (null, 'hello') ;
INSERT INTO #SampleTempTable VALUES (10, null);
INSERT INTO #SampleTempTable VALUES (17, 'abc');
INSERT INTO #SampleTempTable VALUES (17, 'yes');
INSERT INTO #SampleTempTable VALUES (null, null);
GO

SELECT * FROM #SampleTempTable WHERE id IS DISTINCT FROM 17;
DROP TABLE IF EXISTS #SampleTempTable;
GO