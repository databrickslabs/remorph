-- see https://docs.snowflake.com/en/sql-reference/functions/system_external_table_pipe_status

SELECT SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('mydb.myschema.exttable');
