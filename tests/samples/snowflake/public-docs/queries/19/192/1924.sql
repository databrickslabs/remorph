-- see https://docs.snowflake.com/en/sql-reference/functions/system_block_internal_stages_public_access

USE ROLE accountadmin;

SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS();