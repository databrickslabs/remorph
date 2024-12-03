--Query type: DCL
EXECUTE AS USER = 'Sales';
SELECT HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'SELECT') AS HasSelectPermission,
       HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'INSERT') AS HasInsertPermission,
       HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'UPDATE') AS HasUpdatePermission,
       HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'DELETE') AS HasDeletePermission
FROM (VALUES (1)) AS TempTable (Id);
REVERT;
