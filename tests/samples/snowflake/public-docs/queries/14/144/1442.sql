-- see https://docs.snowflake.com/en/sql-reference/functions/system_pipe_force_resume

SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema."myPipe"');