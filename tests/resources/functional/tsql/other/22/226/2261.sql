--Query type: DCL
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'MyDB')
CREATE DATABASE MyDB;

DECLARE @sql nvarchar(max) = 'SELECT * FROM sys.tables';
DECLARE @tables TABLE (name sysname);

INSERT INTO @tables
EXEC ('USE MyDB; ' + @sql);

WITH tables AS (
    SELECT name
    FROM @tables
)
SELECT *
FROM tables;

-- REMORPH CLEANUP: DROP TABLE #tables; DROP DATABASE MyDB;