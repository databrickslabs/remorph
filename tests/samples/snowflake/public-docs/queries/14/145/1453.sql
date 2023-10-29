-- see https://docs.snowflake.com/en/sql-reference/functions/system_task_dependents_enable

SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('mydb.myschema."myTask"');