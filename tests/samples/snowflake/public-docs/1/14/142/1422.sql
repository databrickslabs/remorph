select *
  from table(information_schema.complete_task_graphs (
    result_limit => 10,
    root_task_name=>'MYTASK'));