-- tsql sql:
WITH UserNames AS (
    SELECT 'Mary' AS UserName
)
SELECT 'GRANT VIEW DEFINITION ON FULLTEXT STOPLIST :: dbo.ProductStoplist TO ' + QUOTENAME(UserName) AS sql
INTO #sql_statements
FROM UserNames;

DECLARE @sql nvarchar(max);

DECLARE cur_sql_statements CURSOR FOR SELECT sql FROM #sql_statements;

OPEN cur_sql_statements;

FETCH NEXT FROM cur_sql_statements INTO @sql;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC sp_executesql @sql;
    FETCH NEXT FROM cur_sql_statements INTO @sql;
END

CLOSE cur_sql_statements;

DEALLOCATE cur_sql_statements;

SELECT *
FROM sys.fulltext_stoplists
WHERE name = 'ProductStoplist';

-- REMORPH CLEANUP: DROP TABLE #sql_statements;
