-- see https://docs.snowflake.com/en/sql-reference/functions/task_history

select *
  from table(information_schema.task_history(
    scheduled_time_range_start=>dateadd('hour',-1,current_timestamp()),
    result_limit => 10,
    task_name=>'MYTASK'));