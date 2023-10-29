-- see https://docs.snowflake.com/en/sql-reference/functions/system_verify_ext_oauth_token

SELECT SYSTEM$VERIFY_EXTERNAL_OAUTH_TOKEN('<access_token>');
