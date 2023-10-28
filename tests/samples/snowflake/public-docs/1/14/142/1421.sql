select *
  from table(information_schema.complete_task_graphs())
  order by scheduled_time;