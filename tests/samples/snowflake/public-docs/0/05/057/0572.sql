CREATE VIEW v2 AS
SELECT
  authz_role,
  UPPER(authz_role) AS upper_authz_role
FROM t2;

SELECT IS_ROLE_IN_SESSION(upper_auth_role) FROM v2;