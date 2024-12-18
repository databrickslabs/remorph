-- tsql sql:
WITH database_info AS (
    SELECT 'database_name' AS name, 'ON' AS snapshot_isolation_state, 'ON - ALLOW_SNAPSHOT_ISOLATION' AS snapshot_isolation_state_desc
    UNION ALL
    SELECT 'database_name_2' AS name, 'OFF' AS snapshot_isolation_state, 'OFF - ALLOW_SNAPSHOT_ISOLATION' AS snapshot_isolation_state_desc
)
SELECT name, snapshot_isolation_state,
    snapshot_isolation_state_desc AS description
FROM database_info
WHERE name = 'database_name';
