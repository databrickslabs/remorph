-- see https://docs.snowflake.com/en/sql-reference/functions/is_granted_to_invoker_role

CREATE OR REPLACE MASKING POLICY mask_string AS
(val string) RETURNS string ->
CASE
  WHEN IS_GRANTED_TO_INVOKER_ROLE('ANALYST') then val
  ELSE '*******'
END;