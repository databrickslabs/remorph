--Query type: DQL
WITH cte AS (
    SELECT 'customer' AS type, 'c' AS name
),
     s AS (
    SELECT 'supplier' AS type, 's' AS name
)
SELECT HAS_PERMS_BY_NAME(db_name(), 'DATABASE', 'CREATE VIEW') & HAS_PERMS_BY_NAME('public', 'SCHEMA', 'ALTER') AS _can_create_views,
       HAS_PERMS_BY_NAME(db_name(), 'DATABASE', 'CREATE FUNCTION') & HAS_PERMS_BY_NAME('public', 'SCHEMA', 'ALTER') AS _can_create_funcs
FROM cte, s