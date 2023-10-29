-- see https://docs.snowflake.com/en/sql-reference/functions/complete_task_graphs

select *
  from table(information_schema.complete_task_graphs (
    result_limit => 10,
    root_task_name=>'MYTASK'));