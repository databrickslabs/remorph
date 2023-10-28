select *
  from table(information_schema.serverless_task_history(
    date_range_start=>'2021-10-08 19:00:00.000',
    date_range_end=>'2021-10-08 20:00:00.000'));