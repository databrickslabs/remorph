-- see https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status

SELECT SYSTEM$PIPE_STATUS('mydb.myschema.mypipe');
