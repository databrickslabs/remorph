--Query type: DML
CREATE TABLE #indexes (tablename sysname, objectid int, indexid int, frag decimal(5, 2));
INSERT INTO #indexes (tablename, objectid, indexid, frag)
VALUES ('table1', 1, 1, 10.00), ('table2', 2, 2, 20.00), ('table3', 3, 3, 30.00);
DECLARE @tablename sysname, @objectid int, @indexid int, @frag decimal(5, 2), @execstr nvarchar(100);
DECLARE cur CURSOR FOR SELECT tablename, objectid, indexid, frag FROM #indexes;
OPEN cur;
FETCH NEXT FROM cur INTO @tablename, @objectid, @indexid, @frag;
WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT 'Executing DBCC INDEXDEFRAG (0, ' + RTRIM(@tablename) + ', ' + RTRIM(CONVERT(varchar(10), @indexid)) + ') - fragmentation currently ' + RTRIM(CONVERT(varchar(15), @frag)) + '%';
    SET @execstr = 'DBCC INDEXDEFRAG (0, ' + RTRIM(@objectid) + ', ' + RTRIM(@indexid) + ')';
    EXEC (@execstr);
    FETCH NEXT FROM cur INTO @tablename, @objectid, @indexid, @frag;
END
CLOSE cur;
DEALLOCATE cur;
SELECT * FROM #indexes;
-- REMORPH CLEANUP: DROP TABLE #indexes;
