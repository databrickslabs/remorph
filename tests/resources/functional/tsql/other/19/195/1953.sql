--Query type: DCL
DECLARE @principal sysname = 'public';
DENY EXECUTE ON sys.xp_cmdshell TO public;
SELECT *
FROM sys.database_permissions
WHERE state_desc = 'DENY'
    AND permission_name = 'EXECUTE'
    AND major_id = OBJECT_ID('sys.xp_cmdshell');