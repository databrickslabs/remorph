select *
  from table(information_schema.serverless_task_history(
    date_range_start=>dateadd(H, -12, current_timestamp)));