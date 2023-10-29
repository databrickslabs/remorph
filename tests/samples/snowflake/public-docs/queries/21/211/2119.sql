-- see https://docs.snowflake.com/en/sql-reference/functions/task_history

select *
  from table(information_schema.task_history())
  order by scheduled_time;