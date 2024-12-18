-- tsql sql:
CREATE ROLE [specific_role];
GRANT EXECUTE ON SCHEMA::dbo TO [specific_role];
GRANT CREATE EXTERNAL LIBRARY TO [specific_role];
SELECT *
FROM sys.database_principals AS dp
INNER JOIN sys.database_permissions AS perm
    ON dp.principal_id = perm.grantee_principal_id
WHERE dp.name = 'specific_role';
-- REMORPH CLEANUP: DROP ROLE [specific_role];
