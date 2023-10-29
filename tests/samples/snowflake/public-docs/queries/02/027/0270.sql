-- see https://docs.snowflake.com/en/sql-reference/functions/invoker_role

CREATE OR REPLACE MASKING POLICY mask_string AS
(val string) RETURNS string ->
CASE
  WHEN INVOKER_ROLE() IN ('ANALYST') THEN val
  ELSE '********'
END;