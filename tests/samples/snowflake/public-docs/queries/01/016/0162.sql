-- see https://docs.snowflake.com/en/sql-reference/functions/is_role_in_session

ALTER TABLE allowed_roles
  ADD ROW ACCESS POLICY rap_authz_role_map ON (authz_role);