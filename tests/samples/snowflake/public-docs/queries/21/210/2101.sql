-- see https://docs.snowflake.com/en/sql-reference/functions/pipe_usage_history

select *
  from table(information_schema.pipe_usage_history(
    date_range_start=>dateadd('hour',-12,current_timestamp()),
    pipe_name=>'mydb.public.mypipe'));