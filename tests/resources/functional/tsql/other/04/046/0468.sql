--Query type: DML
SET NOCOUNT ON;

DECLARE @tablename VARCHAR(255);
DECLARE @objectid  INT;
DECLARE @indexid   INT;
DECLARE @frag      DECIMAL;
DECLARE @maxfrag   DECIMAL;

SELECT @maxfrag = 30.0;

CREATE TABLE #fragmentation_list
(
    ObjectName CHAR(255),
    ObjectId INT,
    IndexId INT,
    LogicalFrag DECIMAL
);

WITH tables AS
(
    SELECT 'schema1.table1' AS tablename
    UNION ALL
    SELECT 'schema2.table2' AS tablename
)
INSERT INTO #fragmentation_list (ObjectName, ObjectId, IndexId, LogicalFrag)
SELECT 'schema1.table1', 1, 1, 0.0
UNION ALL
SELECT 'schema2.table2', 2, 2, 0.0;

DECLARE tables_cursor CURSOR FOR
SELECT tablename
FROM (
    SELECT 'schema1.table1' AS tablename
    UNION ALL
    SELECT 'schema2.table2' AS tablename
) AS tables;

OPEN tables_cursor;

FETCH NEXT FROM tables_cursor INTO @tablename;

WHILE @@FETCH_STATUS = 0
BEGIN
    INSERT INTO #fragmentation_list
    EXEC ('DBCC SHOWCONTIG (''' + @tablename + ''') WITH FAST, TABLERESULTS, ALL_INDEXES, NO_INFOMSGS');

    FETCH NEXT FROM tables_cursor INTO @tablename;
END;

CLOSE tables_cursor;
DEALLOCATE tables_cursor;

DECLARE indexes_cursor CURSOR FOR
SELECT ObjectName, ObjectId, IndexId, LogicalFrag
FROM #fragmentation_list
WHERE LogicalFrag >= @maxfrag
    AND INDEXPROPERTY (ObjectId, IndexName, 'IndexDepth') > 0;

OPEN indexes_cursor;

FETCH NEXT FROM indexes_cursor INTO @tablename, @objectid, @indexid, @frag;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT 'Executing DBCC INDEXDEFRAG (0, ' + RTRIM(@tablename) + ', ' + RTRIM(@indexid) + ') - fragmentation currently ' + RTRIM(CONVERT(varchar(15),@frag)) + '%';

    DECLARE @execstr VARCHAR(400);
    SELECT @execstr = 'DBCC INDEXDEFRAG (0, ' + RTRIM(@objectid) + ', ' + RTRIM(@indexid) + ')';
    EXEC (@execstr);

    FETCH NEXT FROM indexes_cursor INTO @tablename, @objectid, @indexid, @frag;
END;

CLOSE indexes_cursor;
DEALLOCATE indexes_cursor;

DROP TABLE #fragmentation_list;
-- REMORPH CLEANUP: DROP TABLE #fragmentation_list;