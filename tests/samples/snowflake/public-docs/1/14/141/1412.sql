select *
  from table(information_schema.serverless_task_history(
    date_range_start=>dateadd(D, -7, current_date),
    date_range_end=>current_date,
    task_name=>'mydb.myschema.mytask'));