--Query type: DDL
CREATE TABLE #TempResult ( CatalogDescription xml );
INSERT INTO #TempResult ( CatalogDescription )
VALUES ( '<Sample Catalog Description/>' );
CREATE PRIMARY XML INDEX PXML_TempResult_CatalogDescription
ON #TempResult ( CatalogDescription );
SELECT *
FROM #TempResult;
-- REMORPH CLEANUP: DROP TABLE #TempResult;
