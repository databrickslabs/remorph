-- see https://docs.snowflake.com/en/sql-reference/functions/task_history

select *
  from table(information_schema.task_history(
    scheduled_time_range_start=>to_timestamp_ltz('2018-11-9 12:00:00.000 -0700'),
    scheduled_time_range_end=>to_timestamp_ltz('2018-11-9 12:30:00.000 -0700')));