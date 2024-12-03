--Query type: DDL
CREATE TABLE allowed_roles (authz_role VARCHAR(50));
INSERT INTO allowed_roles (authz_role)
VALUES ('admin'), ('user');
WITH filtered_roles AS (
    SELECT authz_role
    FROM allowed_roles
    WHERE authz_role = 'admin'
)
SELECT * FROM filtered_roles;
-- REMORPH CLEANUP: DROP TABLE allowed_roles;
