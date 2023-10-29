-- see https://docs.snowflake.com/en/sql-reference/functions/system_unblock_internal_stages_public_access

USE ROLE accountadmin;

SELECT SYSTEM$UNBLOCK_INTERNAL_STAGES_PUBLIC_ACCESS();