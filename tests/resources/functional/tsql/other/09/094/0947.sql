--Query type: DDL
CREATE TABLE #db_options
(
    name sysname,
    filename nvarchar(255),
    size int,
    maxsize nvarchar(10),
    filegrowth int
);

INSERT INTO #db_options (name, filename, size, maxsize, filegrowth)
VALUES ('mynewtest', 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\mynewtest.mdf', 200, 'UNLIMITED', 10);

DECLARE @name sysname,
    @filename nvarchar(255),
    @size int,
    @maxsize nvarchar(10),
    @filegrowth int;

SELECT @name = name,
    @filename = filename,
    @size = size,
    @maxsize = maxsize,
    @filegrowth = filegrowth
FROM #db_options;

DECLARE @sql nvarchar(max) = N'CREATE DATABASE [' + @name + N']
ON PRIMARY
(
    NAME = ''' + @name + ''',
    FILENAME = ''' + @filename + ''',
    SIZE = ' + CONVERT(nvarchar, @size * 8192) + N',
    MAXSIZE = ' + @maxsize + N',
    FILEGROWTH = ' + CONVERT(nvarchar, @filegrowth * 8192) + N'
)
LOG ON
(
    NAME = ''' + @name + '_log'',
    FILENAME = ''C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\' + @name + '_log.ldf'',
    SIZE = 200 * 1024 * 1024,
    MAXSIZE = UNLIMITED,
    FILEGROWTH = 10 * 1024 * 1024
);';

EXEC sp_executesql @sql;

SELECT * FROM #db_options;

DROP TABLE #db_options;
-- REMORPH CLEANUP: DROP DATABASE mynewtest;
