--Query type: DML
CREATE PROCEDURE usp_NestLevelValues_Demo
AS
    WITH NestLevels AS (
        SELECT @@NESTLEVEL AS NestLevel
        UNION ALL
        SELECT @@NESTLEVEL + 1
        FROM (VALUES (1)) AS x(y)
        WHERE @@NESTLEVEL < 5
    )
    SELECT NestLevel AS 'Current Nest Level'
    FROM NestLevels
    WHERE NestLevel = @@NESTLEVEL;

    EXEC ('SELECT @@NESTLEVEL + 1 AS OneGreater');

    DECLARE @sql nvarchar(max) = N'SELECT @@NESTLEVEL + 2 as TwoGreater';
    EXEC sp_executesql @sql;

    WITH NestLevels AS (
        SELECT @@NESTLEVEL AS NestLevel
    )
    SELECT * FROM NestLevels;

-- Execute the stored procedure
EXEC usp_NestLevelValues_Demo;

-- REMORPH CLEANUP: DROP PROCEDURE usp_NestLevelValues_Demo;
