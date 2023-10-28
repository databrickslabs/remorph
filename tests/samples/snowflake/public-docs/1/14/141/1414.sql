select *
  from table(information_schema.task_history())
  order by scheduled_time;