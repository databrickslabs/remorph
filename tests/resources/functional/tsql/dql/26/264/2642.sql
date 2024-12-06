-- tsql sql:
WITH ServerRoles AS (SELECT 'diskadmin' AS ServerRole, 'Contoso\Pat' AS ServerName)
SELECT IS_SRVROLEMEMBER(ServerRole, ServerName) AS IsMember
FROM ServerRoles;
