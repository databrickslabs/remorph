-- see https://docs.snowflake.com/en/sql-reference/functions/current_task_graphs

select *
  from table(information_schema.current_task_graphs(
    result_limit => 10,
    root_task_name=>'MYTASK'));