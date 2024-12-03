--Query type: DQL
CREATE TABLE #temp (c1 NVARCHAR(32));
INSERT #temp VALUES ('This is a test.');
INSERT #temp VALUES ('This is test 2.');
SELECT HASHBYTES('SHA2_256', c1) FROM #temp;
