--Query type: DML
CREATE PROCEDURE myprocedure
    @permission_type nvarchar(50),
    @object_name nvarchar(100),
    @action nvarchar(50)
AS
BEGIN
    PRINT 'Permission Type: ' + @permission_type;
    PRINT 'Object Name: ' + @object_name;
    PRINT 'Action: ' + @action;
END;

DECLARE @local_permission_type nvarchar(50),
    @local_object_name nvarchar(100),
    @local_action nvarchar(50);

WITH temp_permissions AS (
    SELECT 'TABLE' AS permission_type,
        'table_with_different_owner' AS object_name,
        'INSERT' AS action
)
SELECT TOP 1
    @local_permission_type = permission_type,
    @local_object_name = object_name,
    @local_action = action
FROM temp_permissions;

EXEC myprocedure @local_permission_type, @local_object_name, @local_action;
-- REMORPH CLEANUP: DROP PROCEDURE myprocedure;
