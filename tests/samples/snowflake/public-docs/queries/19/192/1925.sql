-- see https://docs.snowflake.com/en/sql-reference/functions/system_internal_stages_public_access_status

USE ROLE accountadmin;

SELECT SYSTEM$INTERNAL_STAGES_PUBLIC_ACCESS_STATUS();