--Query type: DQL
WITH permissions AS ( SELECT 'DATABASE' AS securable, 'ANY' AS permission ) SELECT HAS_PERMS_BY_NAME('tpch', 'DATABASE', 'ANY') AS has_permission FROM permissions;
