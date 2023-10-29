-- see https://docs.snowflake.com/en/sql-reference/functions/is_role_in_session

CREATE OR REPLACE MASKING POLICY allow_analyst AS (val string)
RETURNS string ->
CASE
  WHEN IS_ROLE_IN_SESSION('ANALYST') THEN val
  ELSE '*******'
END;