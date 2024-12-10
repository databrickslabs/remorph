-- tsql sql:
SET NOCOUNT ON;

CREATE TABLE #tmpdbs
(
    id INT IDENTITY(1, 1),
    [dbid] INT,
    [dbname] sysname,
    isdone BIT
);

CREATE TABLE #tmpfgs
(
    id INT IDENTITY(1, 1),
    [dbid] INT,
    [dbname] sysname,
    fgname sysname,
    isdone BIT
);

INSERT INTO #tmpdbs ([dbid], [dbname], [isdone])
SELECT database_id, name, 0
FROM (
    VALUES (1, 'db1'),
           (2, 'db2'),
           (3, 'db3')
) AS T (database_id, name)
WHERE database_id > 1;

DECLARE @dbid INT,
        @query VARCHAR(1000),
        @dbname sysname,
        @fgname sysname;

WHILE (SELECT COUNT(id) FROM #tmpdbs WHERE isdone = 0) > 0
BEGIN
    SELECT TOP 1 @dbname = [dbname], @dbid = [dbid]
    FROM #tmpdbs
    WHERE isdone = 0;

    SET @query = 'SELECT ' + CAST(@dbid AS NVARCHAR) + ', ''' + @dbname + ''', [name], 0
    FROM (
        VALUES (''FG1''),
               (''FG2''),
               (''FG3'')
    ) AS T ([name])
    WHERE [name] = ''FG1'' AND [name] NOT IN (''FG2'')';

    INSERT INTO #tmpfgs
    EXEC (@query);

    UPDATE #tmpdbs
    SET isdone = 1
    WHERE [dbid] = @dbid;
END;

IF (SELECT COUNT(ID) FROM #tmpfgs) > 0
BEGIN
    WHILE (SELECT COUNT(id) FROM #tmpfgs WHERE isdone = 0) > 0
    BEGIN
        SELECT TOP 1 @dbname = [dbname], @dbid = [dbid], @fgname = fgname
        FROM #tmpfgs
        WHERE isdone = 0;

        SET @query = 'ALTER DATABASE [' + @dbname + '] MODIFY FILEGROUP [' + @fgname + '] AUTOGROW_ALL_FILES;';

        PRINT @query;

        UPDATE #tmpfgs
        SET isdone = 1
        WHERE [dbid] = @dbid AND fgname = @fgname;
    END
END;

SELECT *
FROM #tmpdbs;

SELECT *
FROM #tmpfgs;

DROP TABLE #tmpdbs;

DROP TABLE #tmpfgs;
