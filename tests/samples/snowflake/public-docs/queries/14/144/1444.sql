-- see https://docs.snowflake.com/en/sql-reference/functions/system_pipe_force_resume

SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.stalepipe','staleness_check_override, ownership_transfer_check_override');