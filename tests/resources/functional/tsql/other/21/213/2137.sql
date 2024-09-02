--Query type: DCL
DECLARE @sql NVARCHAR(MAX);
DECLARE cur CURSOR FOR
WITH ObjectsToGrant AS (
    SELECT 'Sales.Orders' AS ObjectName, 'John' AS UserName
)
SELECT 'GRANT VIEW DEFINITION ON ' + ObjectName + ' TO ' + UserName + ';' AS sql
FROM ObjectsToGrant;

OPEN cur;
FETCH NEXT FROM cur INTO @sql;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC sp_executesql @sql;
    FETCH NEXT FROM cur INTO @sql;
END

CLOSE cur;
DEALLOCATE cur;

SELECT * FROM Sales.Orders;

-- REMORPH CLEANUP: DROP TABLE Sales.Orders;
-- REMORPH CLEANUP: DROP USER John;