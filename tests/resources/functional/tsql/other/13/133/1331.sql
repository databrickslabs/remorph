-- tsql sql:
CREATE TABLE #t3 ( c3 nvarchar(20) COLLATE Latin1_General_CI_AS_KS_WS );
INSERT INTO #t3 ( c3 )
VALUES ( N'X' ), ( N'Y' ), ( N'Z' );
SELECT * FROM #t3;
-- REMORPH CLEANUP: DROP TABLE #t3;
