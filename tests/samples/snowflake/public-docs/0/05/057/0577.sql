ALTER TABLE allowed_roles
  ADD ROW ACCESS POLICY rap_authz_role ON (authz_role);