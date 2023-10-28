select *
  from table(information_schema.task_dependents(task_name => 'mydb.myschema.mytask', recursive => false));