-- see https://docs.snowflake.com/en/sql-reference/functions/external_functions_history

select *
  from table(information_schema.external_functions_history(
    date_range_start => dateadd('hour', -12, current_timestamp()),
    function_signature => 'mydb.public.myfunction(integer, varchar)'));