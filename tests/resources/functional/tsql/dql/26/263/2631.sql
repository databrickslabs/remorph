--Query type: DQL
WITH permissions AS (SELECT 'LOGIN' AS perm_type, 'IMPERSONATE' AS perm_name)
SELECT HAS_PERMS_BY_NAME('Ps', perm_type, perm_name)
FROM permissions
