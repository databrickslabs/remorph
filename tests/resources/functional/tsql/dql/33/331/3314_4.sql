-- tsql sql:
CREATE TABLE #temp_result (id INT IDENTITY(1,1));
INSERT INTO #temp_result DEFAULT VALUES;
SELECT IDENT_CURRENT('#temp_result');
-- REMORPH CLEANUP: DROP TABLE #temp_result;
