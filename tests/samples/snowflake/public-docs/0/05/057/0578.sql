CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role_map AS (authz_role string)
RETURNS boolean ->
EXISTS (
  SELECT 1 FROM mapping_table m
  WHERE authz_role = m.key and IS_ROLE_IN_SESSION(m.role_name)
);