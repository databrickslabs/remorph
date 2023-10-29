-- see https://docs.snowflake.com/en/sql-reference/functions/is_role_in_session

CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role AS (authz_role string)
RETURNS boolean ->
IS_ROLE_IN_SESSION(authz_role);