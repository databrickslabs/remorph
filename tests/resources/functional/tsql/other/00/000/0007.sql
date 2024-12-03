--Query type: DDL
SELECT *
INTO #temp
FROM OPENROWSET(BULK 'C:\path\to\your\file.csv', FORMATFILE = 'C:\path\to\your\format.xml', FIRSTROW = 2) AS data;

SELECT *
FROM #temp;

-- REMORPH CLEANUP: DROP TABLE #temp;
