-- see https://docs.snowflake.com/en/sql-reference/functions/system_user_task_cancel_ongoing_executions

SELECT SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS('mydb.myschema."myTask"');