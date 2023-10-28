select *
  from table(information_schema.current_task_graphs())
  order by scheduled_time;