-- see https://docs.snowflake.com/en/sql-reference/functions/complete_task_graphs

select *
  from table(information_schema.complete_task_graphs())
  order by scheduled_time;