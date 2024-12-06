-- tsql sql:
CREATE TABLE demo_table (id INT, name VARCHAR(50));
CREATE ROLE customer_viewer;
GRANT SELECT ON demo_table TO customer_viewer;
WITH granted_permissions AS (
    SELECT 'customer_viewer' AS role_name, 'SELECT' AS permission_name, 'demo_table' AS object_name
)
SELECT * FROM granted_permissions;
