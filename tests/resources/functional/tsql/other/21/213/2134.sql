--Query type: DCL
WITH Privileges AS (
    SELECT 'INSERT' AS Privilege, 'dbo.OrderTable' AS ObjectName, '[Alice]' AS UserName
)
SELECT 'GRANT ' + Privilege + ' ON OBJECT::' + ObjectName + ' TO ' + UserName
FROM Privileges;