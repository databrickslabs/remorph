-- tsql sql:
CREATE ROLE Customer;
CREATE TABLE #CustomerList (
    CustomerName sysname
);
INSERT INTO #CustomerList (
    CustomerName
)
VALUES
    ('Customer1'),
    ('Customer2');
DECLARE @CustomerName sysname;
DECLARE @sql nvarchar(max);
DECLARE Customer_Cursor CURSOR FOR SELECT CustomerName FROM #CustomerList;
OPEN Customer_Cursor;
FETCH NEXT FROM Customer_Cursor INTO @CustomerName;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = 'GRANT CONTROL ON ROLE::Customer TO ' + QUOTENAME(@CustomerName);
    EXEC sp_executesql @sql;
    FETCH NEXT FROM Customer_Cursor INTO @CustomerName;
END
CLOSE Customer_Cursor;
DEALLOCATE Customer_Cursor;
DROP TABLE #CustomerList;
SELECT *
FROM sys.database_principals
WHERE name = 'Customer';
-- REMORPH CLEANUP: DROP ROLE Customer;
-- REMORPH CLEANUP: DROP TABLE #CustomerList;
