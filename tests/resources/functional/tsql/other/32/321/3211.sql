--Query type: DCL
DECLARE cur CURSOR FOR
    SELECT 'DENY VIEW DEFINITION ON ROLE::' + RoleName + ' TO ' + UserName + ' CASCADE;' AS sql
    FROM (
        VALUES ('SalesManager', 'JohnDoe'),
               ('MarketingManager', 'JaneDoe')
    ) AS RolesAndUsers(RoleName, UserName);

DECLARE @sql nvarchar(max);

OPEN cur;

FETCH NEXT FROM cur INTO @sql;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC sp_executesql @sql;
    FETCH NEXT FROM cur INTO @sql;
END

CLOSE cur;

DEALLOCATE cur;