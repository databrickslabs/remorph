ALTER TABLE allowed_roles
  ADD ROW ACCESS POLICY rap_authz_role_map ON (authz_role);